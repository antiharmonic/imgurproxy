#!/usr/bin/env perl

# Written for badsign
# Now version 3 with caching.

no warnings; 
use strict; 
use CGI::Carp qw(fatalsToBrowser); # don't just give Error 500 messages
use CGI;
use LWP; # that which grabs the imgur image

my $dir = "/home/dissonant/dissonantbeats.com/i/cached/";

my $q = CGI->new();
my $user_agent = "ImgurProxy/1.0 Perl/5.10"; # fake imgur info
my $img = $ENV{'QUERY_STRING'}; # get the imgur information

if (-e "$dir/$img") { # cached
	chomp(my $mime = qx!file -i $dir/$img!); #use `file` to get the mimetype
	$mime =~ s/^.*?: //; #process
	$mime =~ s/;.*//; #process more
	$| = 1; # stdout hot
	print "Content-type: $mime\n\n"; #output magic
	use File::Copy;
	copy "$dir/$img", \*STDOUT;
	
} else {

my @header = ('Referer'=>'http://www.dissonantbeats.com/i/', 'User-Agent'=>$user_agent);

# virtual browser
my $browser = LWP::UserAgent->new();

# read the imgur data
my $response = $browser->get('http://i.imgur.com/' . $img, @header);

# post the imgur data from whatever server this is currently residing on
# and don't have to figure out what type of image it is!
print "Content-type: " . $response->header("Content-Type") . "\n\n";

# image data stuck in this object
print $response->content;

#the caching
open my $fh, ">", "cached/$img" or die "$!";
print $fh $response->content;
close $fh;
}

