import schemas
from database import engine, getdb
import models
from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'HELLO'}


@app.get('/posts', status_code=status.HTTP_200_OK,
         response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(getdb)):
    posts = db.query(models.Post).all()
    return posts


@app.get('/posts/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(getdb)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f'Post with id {id} was not found')
    return post


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(getdb)):
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if not post.first():
        raise HTTPException(
            status_code=404, detail=f'Post with id {id} was not found')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(getdb)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f'Post with id {id} was not found')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post('/posts', status_code=status.HTTP_201_CREATED,
          response_model=schemas.PostResponse)
def post_create(post: schemas.PostCreate, db: Session = Depends(getdb)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post('/dictionaries', status_code=status.HTTP_201_CREATED)
def dict_create(dict: schemas.DictCreate, db: Session = Depends(getdb)):
    new_dict = models.Dictionary(name=dict.name)
    new_specs = [
        models.DictionaryEntryFieldSpec(**spec.dict())
        for spec in dict.entry_field_specs
    ]
    db.add(new_dict)
    db.commit()
    db.refresh(new_dict)
    for s in new_specs:
        s.dict = new_dict.id
        db.add(s)
    db.commit()

    return 'DONE'


@app.get('/dictionaries', status_code=status.HTTP_200_OK,
         response_model=List[schemas.DictWithEntries])
def get_dicts(db: Session = Depends(getdb)):
    dicts = db.query(models.Dictionary).all()
    for d in dicts:
        print(d.__dict__)
    return dicts
