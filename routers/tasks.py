from fastapi import APIRouter,Depends,HTTPException,Query
from dependencies import get_connection,get_current_user
from schemas import TaskCreate,TaskUpdate,TaskResponse
from exceptions import TaskNotFound

router=APIRouter(prefix="/tasks",tags=["Tasks"])

@router.get("",response_model=list[TaskResponse])
def get_tasks(
    page:int=Query(default=1,ge=1),limit:int=Query(default=10,ge=1,le=100),completed:bool|None=None,sort:str="id"
    ,connection=Depends(get_connection),current_user=Depends(get_current_user)):
    offset=(page-1)*limit
    allowed_sort_fields={"id","title","completed"}
    descending=sort.startswith("-")
    sort_field=sort.lstrip("-")

    if sort_field not in allowed_sort_fields:
        raise HTTPException(status_code=400,detail="Invalid sort field")

    order="DESC" if descending else "ASC"
    query= """SELECT id,title,completed FROM tasks WHERE user_id=? """

    params=[current_user["id"]]

    if completed is not None:
        query+=" AND completed=?"
        params.append(completed)

    query+=f" ORDER BY {sort_field} {order} LIMIT ? OFFSET ?"
    params.extend([limit,offset])
    rows=connection.execute(query,params).fetchall()
    return [dict(row) for row in rows]


@router.get("/{task_id}",response_model=TaskResponse)
def get_task(task_id:int,connection=Depends(get_connection),current_user=Depends(get_current_user)):
    row=connection.execute("SELECT id,title,completed FROM tasks WHERE id=? AND user_id=?",(task_id,current_user["id"])).fetchone()
    if row is None:
        raise TaskNotFound()
    return dict(row)


@router.post("",response_model=TaskResponse,status_code=201)
def create_task(task:TaskCreate,connection=Depends(get_connection),current_user=Depends(get_current_user)):
    cursor=connection.execute("INSERT INTO tasks(title,user_id) VALUES(?,?)",(task.title,current_user["id"]))
    connection.commit()
    return {"id":cursor.lastrowid,"title":task.title,"completed":False}


@router.patch("/{task_id}",response_model=TaskResponse)
def update_task(
    task_id:int,task:TaskUpdate,connection=Depends(get_connection),current_user=Depends(get_current_user)):
    row=connection.execute("SELECT id FROM tasks WHERE id=? AND user_id=?",(task_id,current_user["id"])).fetchone()
    if row is None:
        raise TaskNotFound()
    connection.execute("UPDATE tasks SET title=COALESCE(?,title),completed=COALESCE(?,completed) WHERE id=? AND user_id=?",(task.title,task.completed,task_id,current_user["id"]))
    connection.commit()
    row=connection.execute(
        "SELECT id,title,completed FROM tasks WHERE id=? AND user_id=?",
        (task_id,current_user["id"])
    ).fetchone()

    return dict(row)


@router.delete("/{task_id}",status_code=204)
def delete_task(
    task_id:int,
    connection=Depends(get_connection),
    current_user=Depends(get_current_user)
):
    cursor=connection.execute(
        "DELETE FROM tasks WHERE id=? AND user_id=?",
        (task_id,current_user["id"])
    )

    connection.commit()

    if cursor.rowcount==0:
        raise TaskNotFound()