from flask import Flask,render_template,request
import sqlite3 as sql
conn=sql.connect('database2.db')
print("Opened database successfully")
try:
    conn.execute('CREATE TABLE Employee (EmployeeID TEXT, Name TEXT, Role TEXT)')
    print ("Table created successfully")
    conn.close()
except sql.OperationalError:
    None

app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            EmployeeID = request.form['EmployeeID']
            Name = request.form['name']
            Role = request.form['Role']

            with sql.connect("database2.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Employee (EmployeeID,Name,Role) VALUES(?, ?, ?, ?)",(EmployeeID,Name,Role) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg)
            con.close()
@app.route('/list')
def list():
    con = sql.connect("database2.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from Employee")
    rows = cur.fetchall();
    return render_template("list.html", rows=rows)
if __name__ == "__main__":
    app.debug = True
    app.run()

