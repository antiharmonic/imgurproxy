#!/usr/bin/perl

# Written for Senor Justin Gardner
# Cause I didn't want to actually work
# Now version 2.0, with CACHING!!!

no warnings; 
use strict;   # *whips out the yardstick*
use CGI::Carp qw(fatalsToBrowser); # don't just give Error 500 messages
use CGI; # lol i don't think I actually used this
use LWP; # what grabs the imgur image

my $dir = "/home/dissonant/dissonantbeats.com/i/cached/";

my $q = CGI->new();
my $user_agent = "ImgurProxy/1.0 Perl/5.10"; # lol fake imgur info
my $img = $ENV{'QUERY_STRING'}; # get the imgur information

if (-e "$dir/$img") { #CACHED :O
	chomp(my $mime = qx!file -i $dir/$img!); #use `file` to get the mimetype
	$mime =~ s/^.*?: //; #process
	$mime =~ s/;.*//; #process HARDER
	$| = 1; #stdout is fucking hot
	print "Content-type: $mime\n\n"; #output magic inc
	use File::Copy;
	copy "$dir/$img", \*STDOUT;
	
} else {

# @HEADer... GET IT
my @header = ('Referer'=>'http://www.dissonantbeats.com/i/', 'User-Agent'=>$user_agent);

# virtual browser
my $browser = LWP::UserAgent->new();

# read the imgur data LIKE A BOSS (reads on the server level, so no one has a chance to block it ;)
my $response = $browser->get('http://i.imgur.com/' . $img, @header);


# post the imgur data from whatever server this is currently residing on (without caching :o (for now))
# yay don't have to figure out what type of image it is!
print "Content-type: " . $response->header("Content-Type") . "\n\n";

# image data stuck in this object, kinda like how i stuck ur mom
print $response->content;

#the caching, the caching, what what, the caching
open my $fh, ">", "cached/$img" or die "$!";
print $fh $response->content;
close $fh;
}

