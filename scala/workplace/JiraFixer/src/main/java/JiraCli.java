import com.atlassian.httpclient.api.HttpClient;
import com.atlassian.httpclient.api.Request;
import com.atlassian.jira.rest.client.api.AuthenticationHandler;
import com.atlassian.jira.rest.client.api.IssueRestClient;
import com.atlassian.jira.rest.client.api.JiraRestClient;
import com.atlassian.jira.rest.client.api.ProjectRestClient;
import com.atlassian.jira.rest.client.api.domain.*;
import com.atlassian.jira.rest.client.api.domain.input.IssueInput;
import com.atlassian.jira.rest.client.api.domain.input.IssueInputBuilder;
import com.atlassian.jira.rest.client.auth.AnonymousAuthenticationHandler;
import com.atlassian.jira.rest.client.auth.BasicHttpAuthenticationHandler;
import com.atlassian.jira.rest.client.internal.async.AsynchronousHttpClientFactory;
import com.atlassian.jira.rest.client.internal.async.AsynchronousJiraRestClient;
import com.atlassian.jira.rest.client.internal.async.DisposableHttpClient;
import io.atlassian.util.concurrent.Promise;
import sun.awt.AWTAccessor;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.concurrent.ExecutionException;

public class JiraCli {
    public static void main(String[] args) throws URISyntaxException, IOException, ExecutionException, InterruptedException {
        URI serverUri = new URI("https://burberry.atlassian.net");
        AsynchronousHttpClientFactory asynchronousHttpClientFactory = new AsynchronousHttpClientFactory();
        BasicHttpAuthenticationHandler basicHttpAuthenticationHandler = new BasicHttpAuthenticationHandler(
                "customerinsight@burberry.com",
                        "fYNoCX3jSsgNy1YyglSZ59CA"
        );

        DisposableHttpClient httpClient = asynchronousHttpClientFactory.createClient(serverUri, basicHttpAuthenticationHandler);
        JiraRestClient jiraRestClient = new AsynchronousJiraRestClient(serverUri, httpClient);
        IssueRestClient issueRestClient = jiraRestClient.getIssueClient();
        ProjectRestClient projectRestClient = jiraRestClient.getProjectClient();
        Promise<Project> projectPromise = projectRestClient.getProject("CDE");
        Project project = projectPromise.claim();
        System.out.println(project.getIssueTypes());
        BasicProject basicProject = new BasicProject(project.getSelf(), project.getKey(), project.getId(),project.getName());
        IssueInputBuilder issueInputBuilder = new IssueInputBuilder();
        BasicUser basicUser = new BasicUser(new URI("https://burberry.atlassian.net/jira/people/5e0f4b6db540b70da8386a22"), "azaparozhtsa", "Aliaksandr_Zaparozhtsau");
        Promise<Issue> issue = issueRestClient.getIssue("CDE-6496");
        issueInputBuilder
                .setProject(basicProject)
                .setIssueType(issue.get().getIssueType());
        Promise<Void> promise = issueRestClient.updateIssue("CDE-6496",issueInputBuilder.build());
        Void res = promise.claim();
        System.out.println(res);
        Issue issue1 = issue.claim();
        User user = issue1.getAssignee();
        System.out.println(issue1.toString());
//        IssueInput issueInput = issueInputBuilder
//                .setProjectKey("CDE")
//                .setPriorityId(2L)
//                .setAssignee(basicUser)
//                .setAssigneeName("Aliaksandr_Zaparozhtsau")
//                .build();
//        Promise promise = issueRestClient.updateIssue("CDE-6496", issueInput);
//        System.out.println(promise.isDone());
    }
}
//server {
//    url  = "https://burberry.atlassian.net" # Jira server URL
//    user = "customerinsight@burberry.com"   # Jira username (email, was 'AP_JIRA_Robot')
//    pass = "fYNoCX3jSsgNy1YyglSZ59CA"       # Jira password (token, was 'BURB-BIGD2017!')
//}