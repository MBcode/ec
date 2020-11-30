
;from csq.py
;#cs=f'/usr/bin/python3 sq2.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
;cs=f'/usr/bin/python3 sq1.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
(defun csq (qry_str)
  (let ((cs (str-cat "/usr/bin/python3 sq2.py " qry_str 
                     "|curl $dcs_url -F \"dcs.output.format=JSON\" -F \"dcs.c2stream=@-\"")))
    (tsh cs)))

;../sca.cl
;need to move fast in getting elts out of jsonLD
(defvar *clowder-host* "https://earthcube.clowderframework.org")
(ql 'dexador) ;github.com/fukamachi/dexador
(ql 'drakma)
(defun safe-url (u)
  (drakma:url-encode u :utf-8))

;from js.cl
(require :cl-json)
;(defun encode-json2str (js) (json:encode-json-to-string js))
(defun encode-json2str (js)
  (if (equal js '(nil)) "[]"
    (json:encode-json-to-string js)))
;(defun decode-json-from-str (str) (json:decode-json-from-string str))
(defun decode-json-from-str (str)
  (if (equal "[]" str) '(nil)
    (json:decode-json-from-string str)))
;
(defun decode-file (path)
    (with-open-file (stream path :direction :input)
          (json:decode-json-strict stream))) 
;
(defun csqj (qry)
  (decode-json-from-str (csq qry)))
;
(defvar *clowder-host* "https://earthcube.clowderframework.org")
(ql 'dexador) ;github.com/fukamachi/dexador
(ql 'drakma)
(defun getLD (id)
  (rest (first-lv
    (decode-json-from-str
     (dex:get (strcat *clowder-host* "/api/datasets/" id "/metadata.jsonld"))))))
; 

(defun tj (&optional (qry ""))
  (print (csqj qry)))

(defun tj2 ()
  ;(file2str "n.js")
  (file2string "n.js")
  )

;need a file2string, that does a file2str and concatenates to one string

(defun tjc- () ;this works w/file2string
  (print (decode-json-from-str  
           (tj2) ;(file2str "n.js")
           )))

(defun tjc ()
  (decode-file "n.js")) ;this works, use to dump ld3.cl

;works, output in ld3.cl to try accessing, maybe, but use csq.py for now
(defvar *j* (tjc))
(defvar *d* (assoc-v :DOCUMENTS *j*))
(defvar *c* (assoc-v :CLUSTERS *j*))
(format t "~%~a docs and ~a clusters~%" (len *d*) (len *c*))
(defun d2id (d)
  (assoc-v :ID d))
(defun d2snip (d)
  (assoc-v :SNIPPET d))
(defun d2nameDes (d)
  (break2lines (d2snip d)))
(defun d2id_nd (d)
  (cons (d2id d) (d2nameDes d)))
(defvar *a* (mapcar #'d2id_nd *d*))
;this works, now just the jsonLD in it, &probably redo quickly in csq.py
(defun d2id_ld (d)
  (let ((id (d2id d)))
    (cons id (getLD id))))
(defvar *aj* (mapcar #'d2id_ld *d*))
