
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
; csq calls sq2.py which also does this qry
(defun qry (str)
  (let ((qry_str (safe-url str)))
    (decode-json-from-str
     (dex:get (strcat *clowder-host* "/api/search?query=" qry_str)))))
;
(defun getLD (id)
  "get jsonLD from clowder for now" ;but could fallback to ~ld:repo/~doi cache on server
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
(defvar *id* (mapcar #'d2id *d*))
(defun d2snip (d)
  (assoc-v :SNIPPET d))
(defun d2nameDes (d)
  (break2lines (d2snip d)))
(defun d2id_nd (d)
  (cons (d2id d) (d2nameDes d)))
(defvar *a* (mapcar #'d2id_nd *d*)) ;id2nd
;this works, now just the jsonLD in it, &probably redo quickly in csq.py
(defun d2id_ld (d)
  (let ((id (d2id d)))
    (cons id (getLD id))))
(defvar *aj* (mapcar #'d2id_ld *d*)) ;id2ld
;next get sub-topic tags, also in a alst (or py dict); or ht,w/append-value
 ;then create the div's to display the name,description, w/final&clowder/description URLs &tags
;might end w/short set of normalized metadata instead-of/w/ the jsonLD
(defun id2nd (id) 
  "name+descritpion"
  (assoc-v id *a*))

(defun id2ld_ (id) 
  "get jsonLD for id"
  (assoc-v id *aj*))
(defun id2ld (id) 
  "get jsonLD content for id"
  (assoc-v :CONTENT (id2ld_ id)))

(defun id2jld (id) 
  "get jsonLD string"
  (encode-json2str (id2ld id)))

(defun ld2id (ld)
  (assoc-v :IDENTIFIER ld))
(defun ld2dp (ld)
  (assoc-v :DATE-PUBLISHED ld))
;-
(defvar *q* (qry "organic")) ;the part that kicks off making n.js(the clustered output of this qry)
(defun get-id (h) (assoc-v :ID h))
(defun get-name (h) (assoc-v :NAME h))
(defun get-des (h) (assoc-v :DESCRIPTION h))
;could go through&make a map from this,or just get cluster info tags stored/doc&print while htm
;I like that this has the spaces, so could map to repo&..probably doi
;-
(defun c2tp (c)
  (assoc-v :PHRASES c))
(defun c2dl (c)
  (assoc-v :DOCUMENTS c))
(defun add-dt (id tp)
  "add tagphrase to doc" ;right now just print, put append tags2that or similar map
  (let* ((nd (id2nd id)))
    (format nil  "~% ~a gets:~a" (first-lv nd) tp)
    ;if i was asserting it would be doi has-tag tag
      ;see abt alst push value ;in this or the py version get value,append &reset,esp py dict
       ;this is working in csq.py ;by putting in the docs dict,..
    ))
(defun c2id_tp (c)
  "cluster2 id2tag-phrases"
  (let* ((tp (c2tp c))
         (dl (c2dl c)))
    (mapcar #'(lambda (d) (add-dt d tp)) dl)))

(defvar *ct* (mapcar #'c2id_tp *c*)) ;this or a version or ret, used as tags to go below
;-
(defun id2md (id) 
  "get few from ld"
  (let* ((ld (id2ld id))
         (ident (ld2id ld))
         (idv (assoc-v :VALUE (first-lv ident)))
         (dp (ld2dp ld))
         )
    (format nil "~% ~a date:~a"  (or idv ident) dp)))
; (id2md "5f82862ee4b0b81250e016a8")
;urn:doi10.1594/PANGAEA.126048 date:2003

(defvar *f* (mapcar #'id2md *id*)) ;in the end this will dump all the html for search,in py

;if clowder specific could just take this last bit where we get the tags for each doc
 ;then when iteract over original clowder json, to turn into html,   do the getjsonLD and dump that tags too
;could go through *q* and lookup in *ct* the tags to put into the present html divs
