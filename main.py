from models.tarea import Tarea, SessionLocal
import argparse
from functools import wraps

def agregar_tarea(descripcion):
    session = SessionLocal()
    nueva_tarea = Tarea(descripcion=descripcion)
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    session.close()
    return nueva_tarea

def listar_tareas():
    session = SessionLocal()
    tareas = session.query(Tarea).all()
    session.close()
    return tareas

def prioridad_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.prioridad = input('Ingrese la Priordad: ')
        session.commit()
        session.refresh(tarea)
    session.close()
    return tarea

def completar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()
        session.refresh(tarea)
    session.close()
    return tarea

def eliminar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        session.commit()
        resultado = True
    else:
        resultado = False
    session.close()
    return resultado

def buscar_tareas(termino):
    session = SessionLocal()
    tareas = session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()
    session.close()
    return tareas

def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas")
    parser.add_argument('--agregar', type=str, help="Agregar una nueva tarea")
    parser.add_argument('--completar', type=int, help="Marcar una tarea como completada")
    parser.add_argument('--eliminar', type=int, help="Eliminar una tarea")
    parser.add_argument('--buscar', type=str, help="Buscar tareas por descripción")
    parser.add_argument('--listar', action='store_true', help="Listar todas las tareas")
    parser.add_argument('--prioridad', type=int ,help="Marcar Prioridad")

    args = parser.parse_args()

    if args.agregar:
        tarea = agregar_tarea(args.agregar)
        print(f"Tarea agregada: {tarea}")
    elif args.completar:
        tarea = completar_tarea(args.completar)
        if tarea:
            print(f"Tarea completada: {tarea}")
        else:
            print("Tarea no encontrada")
    elif args.eliminar:
        if eliminar_tarea(args.eliminar):
            print("Tarea eliminada")
        else:
            print("Tarea no encontrada")
    elif args.buscar:
        tareas = buscar_tareas(args.buscar)
        print("Tareas encontradas:", tareas)
    elif args.listar:
        tareas = listar_tareas()
        print("Todas las tareas:", tareas)
    #elif args.prioridad:
      #  tarea= prioridad_tarea(args.prioridad)
      #  print("La prioridad editada", tarea)




if __name__ == "__main__":
    main()