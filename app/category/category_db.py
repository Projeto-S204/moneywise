from sqlalchemy import create_engine, Column, Integer, String # type: ignore
from sqlalchemy.orm import declarative_base, sessionmaker # type: ignore

# Configuração da conexão com o banco de dados
DATABASE_URL = "postgresql://usuario:senha@localhost/nome_do_banco"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Category(Base):
    __tableName__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

#Criar a tabela no banco de dados  (caso ainda não exista)
Base.metadata.create_all(bind=engine)

#3Classe CRUD para operações em categories
class CategoryCRUD:

    @staticmethod
    def create_category(name: str):
        """Cria uma nova categoria"""
        session = SessionLocal()
        try:
            new_category = Category(name=name)
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
            return f"Categoria '{new_category.name}' criada com sucesso!"
        except Exception as e:
            session.rollback()
            return f"Erro ao criar categoria: {e}"
        finally:
            session.close()

    @staticmethod
    def get_all_categories():
        """Retorna todas as categorias"""
        session = SessionLocal()
        try:
            categories = session.query(Category).all()
            return [{"id":cat.id, "name":cat.name} for cat in categories]
        except Exception as e:
            return f"Erro ao buscar categorias: {e}"
        finally:   
            session.close()
    
    @staticmethod
    def get_category_by_id(category_id: int):
        """Retorna uma categoria pelo ID"""
        session = SessionLocal()
        try: 
            category = session.query(Category).filter(Category.id == id).first()
            if category: 
                return {"id":category.id, "name":category.name}
            return "Categoria não encontrada"
        except Exception as e:
            return f"Erro ao buscar categoria: {e}"
        finally:
            session.close()

    @staticmethod
    def update_category(category_id:int, new_name:str):
        """Atualiza o nome de uma categoria"""
        session = SessionLocal()
        try:
            category = session.query(Category).filter(Category.id == category_id).first()
            if category:
                category.name = new_name
                session.commit()
                return f"Nome da categoria '{category.name}' atualizado com sucesso!"
            return "Categoria não encontrada"
        except Exception as e:
            session.rollback()
            return f"Erro ao atualizar categoria: {e}"
        finally:
            session.close()
    
    @staticmethod
    def delete_category(category_id: int):
        """Deleta uma categoria pelo ID"""
        session = SessionLocal()
        try:
            category = session.query(Category).filter(Category.id == category_id).first()
            if category:
                session.delete(category)
                session.commit()
                return f"Categoria ID {category_id} deletada com sucesso."
            return f"Categoria com ID {category_id} não encontrada."
        except Exception as e:
            session.rollback()
            return f"Erro ao deletar categoria: {e}"
        finally:
            session.close()
