#!/usr/bin/perl 

print "Content-Type: text/html\r\n\r\n";
my $query_string = $ENV{'QUERY_STRING'};
my @pairs = split(/&/, $query_string);

foreach(@pairs)
{
   my($key, $value) = split(/=/, $_, 2);
   $param{$key} = $value;
}

$filename = $param{'file'};
print $filename;
print " is the file we are examining.";

if (!-e $filename) {
   print " It has failed to load. Recheck spelling of file.";
   exit;
}
if (!length $param{'q'}) {
$html = <<END;
<!DOCTYPE HTML>
<html>
   <body>
      <h1>Error, did not input strings correctly, if at all.</h1>
   </body>
</html>
END
print $html;
exit;
}

$html = <<END;
<!DOCTYPE HTML>
<html>
   <head>
      <title>CS 410 Webserver:</title>
      <style type="text/css">
	 img.displayed 
	 {
            margin-right: auto;
            margin-left: auto;
            display:block;

         }
         h1 
	 { 
               text-align:center;
	       font-size: 16;
               color:red;

         }
      </style>
   </head>
   <body>
      <h1>CS 410 Webserver</h1>
      <br>
      <img class="displayed" src="/my-histogram.cgi?$query_string">
   </body>
</html>
END

print $html;
