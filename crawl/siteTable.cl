;Also have w/py pandas, &could be more fine grain, but this was quick sites2~table script
;df=pd.read_table('cdf_cndls.tsv') print(df[0:18].to_html()) ;mbobak@illinois.edu
;The formatting will change, incl maybe going into a real table, in an about.html page
(defvar *is* " style=\"max-width: 80px; max-height: 40px\" ")
(ql 'cl-csv)
(defvar *csv* (cl-csv:read-csv #P"CDF_Sites.csv"))
(defvar *c1* (first *csv*)) ;headings
(defvar *cf* (rest *csv*))  ;rest of csv
(defvar *c* (subseq *cf* 0 18)) ;was 17
(defvar *c2* (first *c*)) ;for testing
(defun ldns (l &optional (hover t))
  "format:logo domain-name summary"
  (let ((repo (nth 0 l))
        (logo (nth 11 l))
        (domain (nth 7 l))
        (num_datasets (nth 4 l))
        (name (nth 6 l))
        (summary (nth 13 l)))
    ;   (format nil "~%<br><div title=\"~a\"><img ~a src=~a></div><a href=~a>~a</a>" 
    ;           summary *is* logo domain name )
    (if hover
        ;format nil "~%<div title=\"~a\"><a href=~a><img ~a src=~a></div>~a</a>," 
       (format nil 
       "~%<td><div title=\"~a, ~a records\"><a href=~a><img ~a src=~a></div>~a</a></td>" 
                summary num_datasets domain *is* logo (or name repo) )
        (format nil "~%<br><img ~a src=~a><a href=~a>~a</a>,~a" *is* logo
                domain name summary)
    )))

(defun pt (lol)
  "print table"
  (mapcar #'ldns lol))

(defun tp (&optional (lol *c*))
  "test print"
  (pt lol))

(defun stc (&optional (fn "cc.htm"))
  "save(test)table"
  (save-lines (tp) fn))
