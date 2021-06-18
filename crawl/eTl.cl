;The Transform part of ETL, want to start to get rid of redundancy in the blank-node info, and get more entities
; have earlier code that calls some python/rdflib but using jena's riot and a uri lib, here then in py should work too
;Also looking at py:dedupe etc, ..
(defun uri-p (s)
  (eq (search "<" s) 0))

(ql 'quri)

(defun s2uri (s)
  "all strings that are URIs turned to instances"
  (if (not (uri-p s)) s
    (quri:uri (string-trim '(#\< #\>) s))))

(defun rest3 (l)
  "all elts past2 collected into 1 list"
  (if (len_gt l 3) 
    (list (first l) (second l) (subseq l 2))
    l))

;(trace rest3)

(defun parse-nt-line (s) 
 ;(mapcar #'s2uri (split-string s))
  (let ((l (mapcar #'s2uri (split-string s))))
    (rest3 (butlast l))))


(defun riot (fn)
  "jena riot on file,to list of triple-lists"
  (let ((rs (tsh (strcat "riot " fn))))
    (when (len-gt rs 99)
      (let* ((rl (break2lines rs)) ;get list of lines as strings
             ;(rl3 (mapcar #'split-string rl)) ;splits the literal-strs too,   so..
             (rl3 (mapcar #'parse-nt-line rl)) ;splits the literal-strs too,   so..
             )
        ;(mapcar #'butlast 
                (rm-nils rl3)))));)

(defun tr (&optional (fn "hydroshare/f16c8715b349b78d0a3c6ebd2c0eb450d99649ac.jsonld"))
  (riot fn))
