from vpython import *

#define the value of G
G=6.673e-11

## Acceleration of object a due to object b because of their gravitational interaction
def acc(a, b):
    rel_pos = b.pos - a.pos
    return G*b.mass * norm(rel_pos)/rel_pos.mag2

## Accelaration of a due to all the objects b interacting with it
def totalacc (a, objlist):
    sum_acc = vector (0,0,0)
    for b in objlist:
        if (a!=b):
            sum_acc = sum_acc + acc(a, b)
    return sum_acc

#Solar system on a computer

#Constants that we will need
#define the value of G
G=6.673e-11
myPi = 3.141592

boost_j=1.0 #allow for boosting Jupiter's mass
boost_e=1.0 #allow for boosting Earth's mass
boost_s=1.0 #allow for boosting Sun's mass
boost_S=1.0 #allow for boosting Saturn's mass
boost_M=1.0 #allow for boosting Mars' mass

#for initial conditions
jupiter_mass=boost_j*1.9e27
earth_mass=boost_e*6e24
sun_mass=boost_s*2e30
saturn_mass = boost_S*5.68e26 
mars_mass   = boost_M*6.39e23

#=================================================
massive_mass1 = 2.446e29 #mass of Proxima Centauri
#=================================================

AU = 149.6e9       #mean earth sun orbital distance

earth_vel   = 2* myPi *AU/(365.25 *24. *60.*60.) # average velocity = 2*Pi*R/T
jupiter_vel = 2* myPi *AU*5.2/(11.86*365.25*24.*60.*60)
saturn_vel  = 2* myPi *AU*9.5/(29.46*365.25 *24. *60.*60.)
mars_vel    = 2* myPi *AU*1.5/(1.88*365.25 *24. *60.*60.)

#setting for animations
scene.background = color.black
scene.autoscale = 0
scene.range = 30*AU

#objects making up our solar system
sun        = sphere(pos= vector(0,0,0), velocity = vector(0,0,0),
             mass=sun_mass, radius = 0.1*AU, color =color.yellow)
earth      = sphere(pos= vector(AU, 0, 0), velocity = vector(0,earth_vel,0),
               mass=earth_mass, radius=0.05*AU, color =color.blue)
jupiter    = sphere(pos=vector(-5.2*AU,0,0),velocity=vector(0,-jupiter_vel,0),
             mass=jupiter_mass, radius=0.15*AU, color=color.white)
mars       = sphere(pos=vector( 1.5*AU,0,0),velocity=vector(0,mars_vel,0),
             mass=mars_mass, radius=0.001*AU, color=color.red)
saturn     = sphere(pos=vector(-9.5*AU,0,0),velocity=vector(0,-saturn_vel,0),
             mass=saturn_mass, radius=0.01*AU, color=color.green)
P_centauri = sphere(pos=vector( 30*AU,30*AU,30*AU),velocity=vector(-4000,-4000,-4000),
             mass=massive_mass1, radius=0.05*AU, color=color.purple)

#Create a list of objects making up our solar system 
#and add attributes for their accelaration and orbits

bodies = [sun, earth, mars, jupiter, saturn, P_centauri] 

for b in bodies:
    b.acc = vector(0,0,0)
    b.track=curve (color = b.color)

# set total momentum of system to zero (centre of mass frame) 
sum=vector(0,0,0)
for b in bodies:
    if (b!=sun):
        sum=sum+b.mass*b.velocity

sun.velocity=-sum/sun.mass

# dt corresponds to 3000 mins here
dt=30.*60.*100

#Initialize leap-frog by finding the velocites at t=dt/2

for b in bodies:
    b.velocity = b.velocity + totalacc(b, bodies)*dt/2.0

#start leap-frog
while True:
    rate(50)  #optimum value for rate
    for b in bodies:
        #update the positions
        b.pos = b.pos + b.velocity*dt
        b.track.append(pos=b.pos)

        #update the velocities
        b.velocity = b.velocity + totalacc(b, bodies)*dt

    scene.center = vector(0,0,0) #view centered on the origin of CM coord system
