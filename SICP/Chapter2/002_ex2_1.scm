(define (make-rat n d)
	(let ((g (gcd (abs n) (abs d))))
		(if (< d 0)
			(cons (- (/ n g)) (- (/ d g)))
			(cons (/ n g) (/ d g)))))
			
(define (abs x)
	(cond ((> x 0) x)
		  ((= x 0) 0)
		  ((< x 0) (- x))))

(define (gcd a b)
	(if (= b 0)
		a
		(gcd b (remainder a b))))
	   
(define (print-rat x)
	(newline)
	(display (numer x))
	(display "/")
	(display (denom x)))