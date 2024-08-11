---


---

<h3 id="create-a-script">Create a script</h3>
<ol>
<li>
<p>Open a terminal and navigate to the directory where you want to save the script for checking if PC online.</p>
</li>
<li>
<p>Create a new script file called<br>
<code>nano heartbeat.sh</code></p>
</li>
<li>
<p>Add the following content to the sh script:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token shebang important">#!/bin/bash</span>

<span class="token comment"># Use the EMAIL environment variable for recipients</span>
recipients<span class="token operator">=</span><span class="token variable">$EMAIL</span>

<span class="token comment"># Define the subject and message</span>
subject<span class="token operator">=</span><span class="token string">"Heartbeat: PC is online"</span>
message<span class="token operator">=</span><span class="token string">"This is a notification to confirm that the PC is online. Sent at <span class="token variable"><span class="token variable">$(</span><span class="token function">date</span><span class="token variable">)</span></span>."</span>

<span class="token keyword">echo</span> <span class="token string">"<span class="token variable">$message</span>"</span> <span class="token operator">|</span> mail -s <span class="token string">"<span class="token variable">$subject</span>"</span> <span class="token string">"<span class="token variable">$recipients</span>"</span>
</code></pre>
<p>This script will send the email to all the addresses listed in the <code>EMAIL</code> environment variable.</p>
</li>
<li>
<p><strong>Save and close the script:</strong></p>
<ul>
<li>Press <code>CTRL + O</code> to save.</li>
<li>Press <code>Enter</code> to confirm the file name.</li>
<li>Press <code>CTRL + X</code> to exit.</li>
</ul>
</li>
</ol>
<h3 id="ensure-the-email-environment-variable-is-set"><strong>Ensure the <code>EMAIL</code> Environment Variable is Set</strong></h3>
<p>Ensure that your <code>EMAIL</code> environment variable is set correctly in your <code>.bashrc</code> or <code>.profile</code>. For example:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">export</span> EMAIL<span class="token operator">=</span><span class="token string">"pantelis@example.com,email2@example.com,email3@example.com"</span>
</code></pre>
<p>After adding this, make sure to reload your shell configuration:</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">source</span> ~/.bashrc
</code></pre>
<h3 id="set-up-the-cron-job"><strong>Set Up the Cron Job</strong></h3>
<p>If you haven’t already set up the cron job, do it as follows:</p>
<ol>
<li>
<p><strong>Open the crontab file:</strong></p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">crontab</span> -e
</code></pre>
</li>
<li>
<p><strong>Add the cron job:</strong></p>
<pre class=" language-bash"><code class="prism  language-bash">0 * * * * /home/yourusername/heartbeat.sh
</code></pre>
<p>Replace <code>/home/yourusername/heartbeat.sh</code> with the path to the script from 2.</p>
</li>
<li>
<p><strong>Save and exit the crontab editor:</strong></p>
<ul>
<li>Press <code>CTRL + O</code> to save.</li>
<li>Press <code>Enter</code> to confirm.</li>
<li>Press <code>CTRL + X</code> to exit.</li>
</ul>
</li>
</ol>
<h3 id="test-the-setup"><strong>Test the Setup</strong></h3>
<p>You can test if everything works by manually running the script:</p>
<pre class=" language-bash"><code class="prism  language-bash">./heartbeat.sh
</code></pre>
<p>Check your inboxes for the email. If you receive the test email at all specified addresses, the setup is correct.<br>
Ensure that the cron job is working as expected by checking your email every hour in the firstt few hours of running it and verifying that the messages are being sent to all the recipients.</p>

