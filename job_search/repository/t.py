from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from entities.job_entity import Job, Company, Restriction


engine = create_engine('sqlite:///database/app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    job = Job(title='test')
    c = Company(name='olympus')
    job.company = c

    job2 = Job(title='god')
    c2 = Company(name='bic')
    job2.company = c2

    r = Restriction(name='no eating allowed')
    r2 = Restriction(name='no fooling around')
    job3 = Job(title='janitor', restrictions=[r, r2])
    job3.company = c

    session.add(job)
    session.add(job2)
    session.add(job3)
except exc.IntegrityError:
    pass

job4 = Job(title='Guitar Hero')
c4 = session.query(Company).filter(Company.name == 'bic').first()
job4.company_id = c4.id
session.add(job4)

session.commit()
