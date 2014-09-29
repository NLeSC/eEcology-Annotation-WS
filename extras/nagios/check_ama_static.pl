#!/usr/bin/perl

use strict;

my $wget = '/usr/bin/wget --user=guest --password=guest --output-document=tmp_html --no-check-certificate -S';
# Devel url
my $url = 'https://annotation.e-ecology.cloudlet.sara.nl/aws/static/table.js';
# Staging url
# my $url = 'https://public-dev.e-ecology.sara.nl/aws/static/table.js';
# Production url
# my $url = 'https://public.e-ecology.sara.nl/aws/static/table.js';
my @OK = ("200");
my @WARN = ("400", "401", "403", "404", "408");
my @CRITICAL = ("500", "501", "502", "503", "504");

my $TIMEOUT = 20;

my %ERRORS = ('UNKNOWN' , '-1',
              'OK' , '0',
              'WARNING', '1',
              'CRITICAL', '2');

my $state = "CRITICAL";
my $answer = "";

$SIG{'ALRM'} = sub {
     print ("ERROR: check_url Time-Out $TIMEOUT s \n");
     exit $ERRORS{"UNKNOWN"};
};
alarm($TIMEOUT);

system ("$wget $url 2>tmp_res1");
for (1..1000){
}

if (! open STAT1, "tmp_res1") {
  print ("$state: $wget returns no result!");
  exit $ERRORS{$state};
}
close STAT1;

`cat tmp_res1|grep 'HTTP/1'|tail -n 1 >tmp_res`;
open (STAT, "tmp_res");
my @lines = <STAT>;
close STAT;

if ($lines[0]=~/HTTP\/1\.\d+ (\d+)( .*)/) {
  my  $errcode = $1;
  my $errmesg = $2;

  $answer = $answer . "$errcode $errmesg";

  if ('1' eq &chkerrwarn($errcode) ) {
    $state = 'WARNING';
  } elsif ('2' eq &chkerrcritical($errcode)) {
    $state = 'CRITICAL';
  } elsif ('0' eq &chkerrok($errcode)) {
    $state = 'OK';
  }
}

sub chkerrcritical {
  my $err = $1;
  foreach (@CRITICAL){
    if ($_ eq $err) { 
      return 2;
    }
  }
return -1;
}


sub chkerrwarn {
  my $err = $1;
  foreach (@WARN){
    if ($_ eq $err) { 
      return 1;
    }
  }
return -1;
}

sub chkerrok {
  my $err = $1;
  foreach (@OK){
    if ($_ eq $err) { 
      return 0;
    }
  }
return -1;
}

`rm tmp_html tmp_res tmp_res1`;

print ("$state: $answer\n");
exit $ERRORS{$state};
