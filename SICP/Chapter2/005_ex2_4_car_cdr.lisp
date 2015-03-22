(define (raycons x y)
  (lambda (m) (m x y)))

(define (raycar z)
  (z (lambda (p q) p)))

(define (raycdr z)
  (z (lambda (p q) q)))
