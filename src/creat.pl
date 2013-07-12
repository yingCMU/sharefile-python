use strict;
use warnings;

use ElectricCommander;
use HTML::Entities;
use HTTP::Request;
use LWP::UserAgent;

my $agent = LWP::UserAgent->new;
$agent->credentials('electriccloud.zendesk.com:443', 'Web Password', '$[/myProject/zendesk_username]' => '$[/myProject/zendesk_password]');

my $ec = new ElectricCommander();

my $email = $ec->getProperty('Email')->findvalue('/responses/response/property/value');
my $name = $ec->getProperty('Name')->findvalue('/responses/response/property/value');
my $escaped_email = encode_entities($email);
my $escaped_name = encode_entities($name);

my $request = HTTP::Request->new(POST => 'https://electriccloud.zendesk.com/users.xml');
my $content = <<XML;
<user>
  <email>$escaped_email</email>
  <name>$escaped_name</name>
  <roles>0</roles>
  <restriction-id>4</restriction-id>
  <organization-id>20472083</organization-id>
</user>
XML

$request->content_type('application/xml');
$request->content($content);

my $response = $agent->request($request);
if (! $response->is_success())
{
  $ec->setProperty({'propertyName' => '/myParent/_zendesk_action', 'value' => 'failed'});
  die('Error: ', $response->header('WWW-Authenticate') || 'Error accessing',
    "\n", $response->status_line, "\nAborting.");
}