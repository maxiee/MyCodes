(defun ask ()
  (format t "告诉我，这么晚了你为何还不睡？")
  (read))

(defun ask-answer ()
  (format t "哦，~A~%睡你麻痹，起来嗨！" (ask)))
