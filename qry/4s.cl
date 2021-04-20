;4s-httpd -p 8000 -X -s -1 cdf
(ql 'cl4store)
(use-package :4store)
;(in-package :4store)
;;(setf *4store-server* "http://localhost:8000/sparql/")
;(setf *4store-server* "http://localhost:8000")
(setf *4store-server* "http://mbobak-ofc.ncsa.illinois.edu:8000")

(defvar *qry* "prefix sschema: <https://schema.org/> \
SELECT distinct ?subj  ?name ?description WHERE { ?subj sschema:name ?name . \
?subj sschema:description ?description . FILTER ( ! isBlank(?subj) ) \
filter ( contains(lcase(concat(?name,?description)), 'carbon') ) } \
GROUP BY ?subj")
;(defvar *r* (4store::sparql-query *qry*))

; (len *r*) 1098
;(save-lines (flat-1 *r*) "carbon.tmp")
;wc carbon.tmp 3294  310525 2334374 carbon.tmp

(defvar *q0* "prefix sschema: <https://schema.org/> \
SELECT distinct ?subj  ?name ?description WHERE { ?subj sschema:name ?name . \
?subj sschema:description ?description . FILTER ( ! isBlank(?subj) ) \
filter ( contains(lcase(concat(?name,?description)), 'qry') ) } \
GROUP BY ?subj")
(defun q1 (w)
  "qry for 1 word"
  (let ((qry (simple-replace-string "qry" w *q0*)))
    (4store::sparql-query qry)))

(defun q2tf (w)
  (let ((r (q1 w)))
    (format t "~%~a, len:~a" w (len r))
    (save-lines (flat-1 r) (strcat w ".tmp"))))

;(q2tf "norway")
;60    9405   69493 norway.tmp

;instead of flat-1, should cat the triple-lists, w/a tab sep, to a .tsv file
 ;not triples lists, but a list of the the values of the vars asked for
 ;could also turn into json, for the faceted search, probably in py
;(defun sparql-query (query &optional (server-url *4store-server*))
;  (tsv-to-lists
;   (4store-request
;    (concatenate 'string server-url "/sparql/")
;    :parameters `(("query" . ,query)
;          ("output" . "text")))))
;could just catch this before the conversion and dump the tsv to a file
;find py client, unless have time this wkend2play w/a lsp recommender

(defun sparql-qry (query &optional (server-url 4store::*4store-server*))
   (4store::4store-request
    (concatenate 'string server-url "/sparql/")
    :parameters `(("query" . ,query)
          ("output" . "text"))))

(defun qry1 (w)
  "qry for 1 word"
  (let ((qry (simple-replace-string "qry" w *q0*)))
    (sparql-qry qry)))

(defun q2tsv (w)
  (let ((r (qry1 w)))
    (format t "~%~a, len:~a" w (len r))
    (save-lines (list r) (strcat w ".tsv"))))

;(q2tsv "norway")
;68K Apr 20 14:36 norway.tsv
;22    9408   69519 norway.tsv

