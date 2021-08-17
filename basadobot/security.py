from basadobot.models import ParienteBasado, session
from sqlalchemy.exc import IntegrityError

def security1(commenter, pariente, recibidor):
    return pariente in commenter.basadosHechos

def security2(basado):
    try:
        parent = session.query(ParienteBasado).filter(ParienteBasado.parentId == basado.parent_id).first()
        try:
            reci = basado.parent().is_robot_indexable
        
        except AttributeError as e:
            reci = basado.parent().author != "None" and basado.parent().body != "[removed]"
        
        name = basado.parent().author

        if not reci or str(name) == str(basado.author):
            return False

        return parent

    except IntegrityError:
        session.rollback()
        return False