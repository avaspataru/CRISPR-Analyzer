#!/usr/bin/perl
use lib './wu-crispr-model';
use format_features_25;

$oligo=$ARGV[0];
$leftflank_numbases=0;
$rightflank_numbases=3;
my ($feat_vals_ref, $feat_names_ref) = format_features_25::get_seq_features($oligo,$leftflank_numbases,$rightflank_numbases);

my @feat_vals = @{$feat_vals_ref};
my $output = join(",",@feat_vals);
print("$output");
