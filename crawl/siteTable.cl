;Also have w/py pandas, &could be more fine grain, but this was quick sites2~table script
;df=pd.read_table('cdf_cndls.tsv')
;print(df[0:18].to_html())
(defvar *is* " style=\"max-width: 80px; max-height: 40px\" ")
(ql 'cl-csv)
(defvar *csv* (cl-csv:read-csv #P"CDF_Sites.csv"))
(defvar *c1* (first *csv*))
(defvar *cf* (rest *csv*))
(defvar *c* (subseq *cf* 0 17))
(defun ldns (l)
  "format:logo domain-name summary"
  (let ((logo (nth 11 l))
        (domain (nth 9 l))
        (name (nth 8 l))
        (summary (nth 13 l)))
    (format nil "~%<br><img ~a src=~a><a href=~a>~a</a>,~a" *is* logo
            domain name summary)))

(defun pt (lol)
  "print table"
  (mapcar #'ldns lol))

(defun tp (&optional (lol *c*))
  "test print"
  (pt lol))

(defun stc (&optional (fn "c.htm"))
  (save-lines (tp) fn))
