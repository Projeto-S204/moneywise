from config import db


def delete_user_logic(user, password):
    if user.check_password(password):
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[ERRO] Falha ao deletar usuário: {e}")
            return False
    return False
