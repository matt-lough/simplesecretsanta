simplesecretsanta
=================

Simple secret santa generates pairs from your xml/json file, sends them an email, and logs all the pairs for you.

How to use
==========

Provide either xml or json with names and addresses.

    <emails>
      <person>
      	<name>Tall man</name>
      	<email>tall_guy@example.com</email>
      </person>
      <person>
      	<name>Short guy</name>
      	<email>short_guy@example.com</email>
      </person>
    </emails>

Change the config at the top of the file to suit your needs.

Run secretSanta.py in the directory of your file and you're done! 