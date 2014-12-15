(define (abs x)
	(cond ((> x 0) x)
		  ((= x 0) 0)
		  ((< x 0) (- x))))

(define (square x) (* x x))

(define (tri x) (* x x x))

(define (good-enough? guess x)
	(< (abs (- (tri guess) x)) 0.001))
	
(define (improve guess x)
	(/ (+ (/ x (square guess))
		  (* guess 2))
	   3))

(define (trit-iter guess x)
	(if (good-enough? guess x)
		guess
		(trit-iter (improve guess x)
					x)))

(define (trit x)
	(trit-iter 1.0 x))