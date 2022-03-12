(define (domain miconic)
  (:requirements :adl :typing)
  (:types passenger - object
          floor - object
		  elevator - object
         )

(:predicates 
(origin ?person - passenger ?floor - floor)
;; entry of ?person is ?floor
;; inertia

(destin ?person - passenger ?floor - floor)
;; exit of ?person is ?floor
;; inertia

(above ?floor1 - floor  ?floor2 - floor)
;; ?floor2 is located above of ?floor1

(boarded ?person - passenger ?elevator - elevator)
;; true if ?person has boarded the lift

(served ?person - passenger)
;; true if ?person has alighted as her destination

(lift-at ?floor - floor ?elevator - elevator)
;; current position of the lift is at ?floor
)


;;stop

(:action stop
  :parameters (?f - floor ?e - elevator)
  :precondition (lift-at ?f ?e)
  :effect (and 
               (forall (?p - passenger) 
                  (when (and (boarded ?p ?e) 
                             (destin ?p ?f))
                        (and (not (boarded ?p ?e)) 
                             (served  ?p))))
               (forall (?p - passenger)                
                   (when (and (origin ?p ?f) (not (served ?p)))
                              (boarded ?p ?e)))))


;;drive up

(:action up
  :parameters (?f1 - floor ?f2 - floor ?e - elevator)
  :precondition (and (lift-at ?f1 ?e) (above ?f1 ?f2))
  :effect (and (lift-at ?f2 ?e) (not (lift-at ?f1 ?e))))


;;drive down

(:action down
  :parameters (?f1 - floor ?f2 - floor ?e - elevator)
  :precondition (and (lift-at ?f1 ?e) (above ?f2 ?f1))
  :effect (and (lift-at ?f2 ?e) (not (lift-at ?f1 ?e))))
)



