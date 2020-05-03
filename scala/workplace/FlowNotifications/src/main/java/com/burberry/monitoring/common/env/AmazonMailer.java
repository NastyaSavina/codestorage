//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package com.burberry.monitoring.common.env;

import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.simpleemail.AmazonSimpleEmailServiceClient;
import com.amazonaws.services.simpleemail.model.Body;
import com.amazonaws.services.simpleemail.model.Content;
import com.amazonaws.services.simpleemail.model.Destination;
import com.amazonaws.services.simpleemail.model.Message;
import com.amazonaws.services.simpleemail.model.SendEmailRequest;
import com.amazonaws.services.simpleemail.model.SendEmailResult;
import com.burberry.monitoring.common.util.LoggingUtil;
import java.util.Collection;
import java.util.Objects;
import org.apache.log4j.Logger;

public class AmazonMailer {
    private static final Logger LOG = LoggingUtil.consoleLogger(AmazonMailer.class.getName());
    private final AmazonSimpleEmailServiceClient emailClient;
    private final String awsAccountName;

    public AmazonMailer(String awsRegion, String awsAccountName, String awsAccessKeyID, String awsSecretAccessKeyID) {
        this.awsAccountName = awsAccountName;
        LOG.info("Generating email client");
        BasicAWSCredentials credentials = new BasicAWSCredentials(awsAccessKeyID, awsSecretAccessKeyID);
        AmazonSimpleEmailServiceClient client = new AmazonSimpleEmailServiceClient(credentials);
        client.setRegion(Region.getRegion(Regions.fromName(awsRegion)));
        LOG.info("Generated region is: " + awsRegion);
        this.emailClient = client;
    }

    public AmazonMailer.EmailBuilder createEmail() {
        return new AmazonMailer.EmailBuilder(this.emailClient, this.awsAccountName);
    }

    public static class Email {
        private final SendEmailRequest request;
        private final AmazonSimpleEmailServiceClient client;

        private Email(SendEmailRequest request, AmazonSimpleEmailServiceClient client) {
            this.request = request;
            this.client = client;
        }

        public void send() {
            SendEmailResult result = this.client.sendEmail(this.request);
            AmazonMailer.LOG.info(String.format("Message sent! (%s)", result.getMessageId()));
        }
    }

    public static class EmailBuilder {
        private final AmazonSimpleEmailServiceClient client;
        private final String accountName;
        private Body body;
        private Content subject;
        private Collection<String> ccRecipients;
        private Collection<String> toRecipients;
        private Collection<String> bccRecipients;

        private EmailBuilder(AmazonSimpleEmailServiceClient client, String accountName) {
            this.client = client;
            this.accountName = accountName;
        }

        public AmazonMailer.EmailBuilder body(String html) {
            this.body = (new Body()).withHtml(new Content(html));
            return this;
        }

        public AmazonMailer.EmailBuilder subject(String subject) {
            this.subject = new Content(subject);
            return this;
        }

        public AmazonMailer.EmailBuilder toRecipients(Collection<String> recipients) {
            this.toRecipients = recipients;
            return this;
        }

        public AmazonMailer.EmailBuilder ccRecipients(Collection<String> recipients) {
            this.ccRecipients = recipients;
            return this;
        }

        public AmazonMailer.EmailBuilder bccRecipients(Collection<String> recipients) {
            this.bccRecipients = recipients;
            return this;
        }

        public AmazonMailer.Email prepare() {
            Destination destination = (new Destination()).withToAddresses((Collection)Objects.requireNonNull(this.toRecipients)).withCcAddresses(this.ccRecipients).withBccAddresses(this.bccRecipients);
            Message message = new Message((Content)Objects.requireNonNull(this.subject), (Body)Objects.requireNonNull(this.body));
            SendEmailRequest request = (new SendEmailRequest()).withSource(this.accountName).withDestination(destination).withMessage(message);
            AmazonMailer.LOG.info("Email prepared");
            return new AmazonMailer.Email(request, this.client);
        }
    }
}
