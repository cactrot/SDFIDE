#! /usr/bin/env python3

# ----------------------------------------------------------------------------
# sdfide: demo.py
# Copyright (c) 2022- juju2013@github
# All rights reserved.
#
# Demonstration of SDFIDE :
#   execute ./demo.py, and change the last line ide.showsdf with any def
#   while the mesh viewer is open, it'll refresh
# ----------------------------------------------------------------------------


from sdfide import ide
from sdf import *

@op3
def mirror2(other, offset):
    def f(p):
        return other(offset - p)
    return f

@op3
def mirror3(other, axis):
    def f(p):
        p *= (1,1,-1)
        return other.orient(axis)(p)
    return orient(f, axis)

def _normalize(a):
    return a / np.linalg.norm(a)

@op3
def mirror(other, point=ORIGIN, normal=UP ):
    x, y, z = _normalize(normal)
    
    matrix = np.array([
        [1-2*x*x,  -2*x*y,  -2*x*z],
        [ -2*x*y, 1-2*y*y,  -2*y*z],
        [ -2*x*z,  -2*y*z, 1-2*z*z],
    ]).T
    def f(p):
        return other(np.dot(p-point, matrix) + point)
    return f
  
def sample():
  f = sphere(1.1) & box(1.7)
  c = cylinder(0.5)
  f -= c.orient(X) | c.orient(Y)  | c.orient(Z)
  return f


def knurling():
  f = rounded_cylinder(1, 0.1, 5)

  # knurling
  x = box((1, 1, 4)).rotate(pi / 4)
  x = x.circular_array(24, 1.6)
  x = x.twist(0.75) | x.twist(-0.75)
  f -= x.k(0.1)

  # central hole
  f -= cylinder(0.5).k(0.1)

  # vent holes
  c = cylinder(0.25).orient(X)
  f -= c.translate(Z * -2.5).k(0.1)
  f -= c.translate(Z * 2.5).k(0.1)
  return f

def gearlike():
  f = sphere(2) & slab(z0=-0.5, z1=0.5).k(0.1)
  f -= cylinder(1).k(0.1)
  f -= cylinder(0.25).circular_array(16, 2).k(0.1)
  return f

def blobby():
  s = sphere(0.75)
  s = s.translate(Z * -3) | s.translate(Z * 3)
  s = s.union(capsule(Z * -3, Z * 3, 0.5), k=1)

  f = sphere(1.5).union(s.orient(X), s.orient(Y), s.orient(Z), k=1)
  return f
  
def weave():
  f = rounded_box([3.2, 1, 0.25], 0.1).translate((1.5, 0, 0.0625))
  f = f.bend_linear(X * 0.75, X * 2.25, Z * -0.1875, ease.in_out_quad)
  f = f.circular_array(3, 0)

  f = f.repeat((2.7, 5.4, 0), padding=1)
  f |= f.translate((2.7 / 2, 2.7, 0))

  f &= cylinder(10)
  f |= (cylinder(12) - cylinder(10)) & slab(z0=-0.5, z1=0.5).k(0.25)
  return f

def gearlike2(n=0.1):
  f = sphere(2) & slab(z0=-0.5, z1=0.5).k(n)
  f -= cylinder(1).k(n)
  f -= cylinder(0.25).circular_array(16, 2).k(n)
  return f

@sdf3
def sines(scale=1, amplitude=1):
  def f(p):
    x, y, z =  p[:,0], p[:,1], p[:,2]
    return np.sin(scale*x)*np.sin(scale*y)*np.sin(scale*z)*amplitude
  return f

g = gearlike2(0.001).twist(0.3)
g |= g.mirror(point=Z*0.6, normal=Z).rotate(2*pi*1/16/2)
herring = g | capped_cylinder(-Z*0.5, Z*1.5, 1.5).k(0.1) - cylinder(1).k(0.1)

bumpy = sphere(2).blend(sines(scale=6, amplitude=0.1))

bumpyherring = herring.blend(sines(scale=6, amplitude=0.1))

ide.showsdf( sample(), samples=2**24 )

#weave().save('out.stl', samples=2**20)
