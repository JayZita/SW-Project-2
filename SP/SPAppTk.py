from SPDb import SPDb
from SPGuiTk import SPGuiTk

def main():
    db = SPDb(init=False, dbName='SPDb.csv')
    app = SPGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()