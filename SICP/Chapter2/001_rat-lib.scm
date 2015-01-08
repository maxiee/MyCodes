(define (make-rat n d) (cons n d))

(define (numer x) (car x))

(define (denom x) (cdr x))

(define (add-rat x y)
	(make-rat (+ (* (numer x) (denom y))
	             (* (numer y) (denom x)))
			  (* (denom x) (denom y))))

(define (sub-rat x y)
	(make-rat (- (* (numer x) (denom y))
	             (* (numer y) (denom x)))
			  (* (denom x) (denom y))))

(define (mul-rat x y)
	(make-rat (* (numer x) (numer y))
	          (* (denom x) (denom y))))
			  
(define (dev-rat x y)
	(make-rat (* (numer x) (numer y))
	          (* (denom x) (denom y))))
			  
(define (equal-rat? x y)
	(= (* (numer x) (denom y))
	   (* (numer y) (denom x))))