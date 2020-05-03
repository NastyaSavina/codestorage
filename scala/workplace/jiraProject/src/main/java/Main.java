import com.atlassian.jira.rest.client.api.AuthenticationHandler;
import com.atlassian.jira.rest.client.api.IssueRestClient;
import com.atlassian.jira.rest.client.api.JiraRestClient;
import com.atlassian.jira.rest.client.api.domain.BasicUser;
import com.atlassian.jira.rest.client.api.domain.Issue;
import com.atlassian.jira.rest.client.api.domain.User;
import com.atlassian.jira.rest.client.api.domain.input.IssueInput;
import com.atlassian.jira.rest.client.api.domain.input.IssueInputBuilder;
import com.atlassian.jira.rest.client.auth.BasicHttpAuthenticationHandler;
import com.atlassian.jira.rest.client.internal.async.AsynchronousHttpClientFactory;
import com.atlassian.jira.rest.client.internal.async.AsynchronousJiraRestClient;
import com.atlassian.jira.rest.client.internal.async.DisposableHttpClient;
import io.atlassian.util.concurrent.Promise;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class Main {
    public static void main(String[] args) throws URISyntaxException, InterruptedException, ExecutionException, MalformedURLException {
        URI serverUri = new URI("https://burberry.atlassian.net");
        String username = "customerinsight@burberry.com";
        String pass = "fYNoCX3jSsgNy1YyglSZ59CA";
        AsynchronousHttpClientFactory asynchronousHttpClientFactory = new AsynchronousHttpClientFactory();
        AuthenticationHandler handler = new BasicHttpAuthenticationHandler(username, pass);
        DisposableHttpClient client = asynchronousHttpClientFactory.createClient(serverUri, handler);
        JiraRestClient cli = new AsynchronousJiraRestClient(serverUri, client);
        Promise<User> user = cli.getUserClient().getUser("Aliaksandr_Zaparozhtsau");

        System.out.println(user.claim().getAccountId());


//        IssueRestClient issueRestClient = cli.getIssueClient();
//
//        String issueKey = "CDE-6496";
//        String accountId = "5e0f4b6db540b70da8386a22";
//        String displayName = "Aliaksandr_Zaparozhtsau";
//        Promise<Issue> issue = issueRestClient.getIssue(issueKey);
//        System.out.println(issue.claim().toString());
//
//        URI self = new URI("https://burberry.atlassian.net/rest/api/2/user?accountId=5e0f4b6db540b70da8386a22");
//        BasicUser myBasicUser = new BasicUser(self, "", displayName, accountId);
////        System.out.println(myBasicUser.isSelfUriIncomplete());
////
//        IssueInput issueInput = new IssueInputBuilder()
//                .setAssignee(myBasicUser)
////                .setAssigneeName("Aliaksandr_Zaparozhtsau")
//                .build();
//
////        System.out.println(issue.claim().getIssueType().getId());
//
//
//        System.out.println(issue.claim().getAssignee().toString());
//
//
//        System.out.println("Ticket type changed successfully");
    }
}

