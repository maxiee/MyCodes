(define (make-rat n d)
	(let ((g (gcd n d)))
		(cons (/ n g) (/ d g))))

(define (gcd a b)
	(if (= b 0)
		a
		(gcd b (remainder a b))))

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
	   
(define (print-rat x)
	(newline)
	(display (numer x))
	(display "/")
	(display (denom x)))