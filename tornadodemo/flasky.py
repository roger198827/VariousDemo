from flask import Flask
app = Flask(__name__)

def P2(n):
    print reduce(lambda x,y:x*y, range(1,n+1))
    return reduce(lambda x,y:x*y, range(1,n+1))

@app.route('/flask')
def hello_world():
    print 'Calc Fac in Flask, result : %d'%P2(6)
    return 'This comes from Flask ^_^'
    