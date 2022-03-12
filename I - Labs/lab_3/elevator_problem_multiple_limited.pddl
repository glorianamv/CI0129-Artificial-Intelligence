


(define (problem mixed-f2-p1-u0-v0-g0-a0-n0-A0-B0-N0-F0-r0)
   (:domain miconic)
   (:objects p0 p1 p2 p3 p4 - passenger
             f0 f1 f2 f3 f4 f5 f6 f7 - floor
			 e0 e1 - elevator)


(:init
(above f0 f1)
(above f0 f2)
(above f0 f3)
(above f0 f4)
(above f0 f5)
(above f0 f6)
(above f0 f7)
(above f1 f2)
(above f1 f3)
(above f1 f4)
(above f1 f5)
(above f1 f6)
(above f1 f7)
(above f2 f3)
(above f2 f4)
(above f2 f5)
(above f2 f6)
(above f2 f7)
(above f3 f4)
(above f3 f5)
(above f3 f6)
(above f3 f7)
(above f4 f5)
(above f4 f6)
(above f4 f7)
(above f5 f6)
(above f5 f7)
(above f6 f7)

(origin p0 f0)
(destin p0 f7)

(origin p1 f0)
(destin p1 f7)

(origin p2 f0)
(destin p2 f7)

(origin p3 f7)
(destin p3 f0)

(origin p4 f7)
(destin p4 f0)

(lift-at f4 e0)
(lift-at f5 e1)

(even f0)
(even f2)
(even f4)
(even f6)
(evenElev e0)

(odd f1)
(odd f3)
(odd f5)
(odd f7)
(oddElev e1)

(div-three f3)
(div-three f6)
(div-threeElev e1)


)


(:goal (forall (?p - passenger) (served ?p)))

)


