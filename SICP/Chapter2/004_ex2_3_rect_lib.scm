(define (make-point x y)
	(cons x y))

(define (x-point p)
	(car p))

(define (y-point p)
	(cdr p))
	
(define (make-rect1 p l w)
	(cons p
	      (cons l w)))

(define (make-rect2 p1 p2)
	(cons p1
	      (cons (- (x-point p2) (x-point p1))
		        (- (y-point p2) (y-point p1)))))

(define (upleft-point rect)
	(car rect))

(define (rect-length rect)
	(car (cdr rect)))

(define (rect-width rect)
	(cdr (cdr rect)))

(define (rect-perimeter rect)
	(* 2 (+ (rect-length rect)
	        (rect-width rect))))

(define (rect-size rect)
	(* (rect-length rect)
	   (rect-width rect)))