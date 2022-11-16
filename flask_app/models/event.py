from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session
from flask_app.models import user

DB='websighting'
class Event:
    def __init__(self,data):
        self.id=data['id']
        self.location=data['location']
        self.what_happened=data['what_happened']
        self.date_of_sighting=data['date_of_sighting']
        self.num_of_sas=data['num_of_sas']
        self.updated_at=data['updated_at']
        self.created_at=data['created_at']
        self.user=None
    @staticmethod
    def is_valid(data):
        valid=True
        flash_string='is required'
        if len(data['location'])<1:
            flash('Location '+ flash_string,'event')
            valid=False
        if len(data['what_happened'])<1:
            flash('What happened '+flash_string,'event')
            valid=False
        if len(data['date_of_sighting'])<1:
            flash('Date of sighting '+flash_string,'event')
            valid=False
        if int(data['num_of_sas'])<=0:
            flash('Number of Sasquatches min 1','event')
            valid=False
        return valid
    @classmethod
    def save_event(cls,data):
        if not Event.is_valid(data):
            return False
        query='''INSERT INTO events(location,what_happened,date_of_sighting,num_of_sas,created_at,updated_at,user_id)VALUES
        (%(location)s,%(what_happened)s,%(date_of_sighting)s,%(num_of_sas)s,NOW(),NOW(),%(user_id)s)'''
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def show_all_event(cls):
        query='SELECT * from events join users on users.id=events.user_id'
        events=[]
        result=connectToMySQL(DB).query_db(query)
        for event in result:
            event_obj=cls(event)
            event_obj.user=user.User({
                'id':event['user_id'],
                'first_name':event['first_name'],
                'last_name':event['last_name'],
                'email':event['email'],
                'password':event['password'],
                'created_at':event['users.created_at'],
                'updated_at':event['users.updated_at']
                 })

            events.append(event_obj)
        return events
    @classmethod
    def by_id(cls,id):
        data={'id':id}
        query='SELECT * FROM events JOIN users ON users.id=events.user_id where events.id=%(id)s'
        result=connectToMySQL(DB).query_db(query,data)
        event=result[0]
        event_obj=cls(event)
        event_obj.user=user.User({
                'id':event['users.id'],
                'first_name':event['first_name'],
                'last_name':event['last_name'],
                'email':event['email'],
                'password':event['password'],
                'updated_at':event['users.updated_at'],
                'created_at':event['users.created_at']

        })
  
        return event_obj
        
      
    @classmethod
    def update_event(cls,data):
        this_event=cls.by_id(data['id'])
        if this_event.user.id!=session['user_id']:
            return False
        if not Event.is_valid(data):
            return False

        query='''UPDATE events SET location=%(location)s,what_happened=%(what_happened)s,date_of_sighting=%(date_of_sighting)s,num_of_sas=%(num_of_sas)s where id=%(id)s'''
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def destroy(cls,id):
        this_event=cls.by_id(id)
        if this_event.user.id!=session['user_id']:
            return False
        data={'id':id}
        query='DELETE FROM events where id=%(id)s'
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def believer(cls,data):
        query='INSERT INTO believer(event_id,user_id)VALUES(%(event_id)s,%(user_id)s)'
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def skeptic(cls,data):
        query='DELETE from believer where user_id=%(user_id)s'
        return connectToMySQL(DB).query_db(query,data)


   