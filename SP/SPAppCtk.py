from SPDb import SPDb
from SPGuiCtk import SPGuiCtk

def main():
    db = SPDb(init=False, dbName='SPDb.csv')
    app = SPGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()