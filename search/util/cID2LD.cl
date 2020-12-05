(defvar *clowder-host* "https://earthcube.clowderframework.org")
(ql 'dexador) ;github.com/fukamachi/dexador
(ql 'drakma)

;splitting out, saying what is clowder
(defun cID2LD (cID)
     (dex:get (strcat *clowder-host* "/api/datasets/" cID "/metadata.jsonld")))

(defun cID2LD_ (cID)
  (let ((ccf (str-cat "cc/" cID ".jsonld")))
    (if (probe-file ccf)
      (file2string ccf)
      (let ((nd (cID2LD cID)))
        (save-lines (list nd) ccf)
        nd))))

(defun gd (id)
  (print (cID2LD_ id)))

