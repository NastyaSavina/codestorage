import com.atlassian.jira.rest.client.api.AuthenticationHandler;
import com.atlassian.jira.rest.client.api.IssueRestClient;
import com.atlassian.jira.rest.client.api.JiraRestClient;
import com.atlassian.jira.rest.client.api.domain.BasicUser;
import com.atlassian.jira.rest.client.api.domain.User;
import com.atlassian.jira.rest.client.api.domain.input.IssueInput;
import com.atlassian.jira.rest.client.api.domain.input.IssueInputBuilder;
import com.atlassian.jira.rest.client.auth.BasicHttpAuthenticationHandler;
import com.atlassian.jira.rest.client.internal.async.AsynchronousHttpClientFactory;
import com.atlassian.jira.rest.client.internal.async.AsynchronousJiraRestClient;
import com.atlassian.jira.rest.client.internal.async.DisposableHttpClient;
import io.atlassian.util.concurrent.Promise;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.*;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class JiraTicketAssignee {
    public static void main(String[] args) throws URISyntaxException {
        String restLogin = "customerinsight@burberry.com";
        String restPass = "fYNoCX3jSsgNy1YyglSZ59CA";
        String username = "Aliaksandr_Zaparozhtsau";

        JiraRestClient cli = getJiraRestClient(restLogin, restPass);

        User user = cli.getUserClient().getUser(username).claim();
        System.out.println(user.toString());
        Map<String, URI> avatarUris = new HashMap<>();
        avatarUris.put("16x16", user.getAvatarUri("16x16"));
        avatarUris.put("24x24", user.getAvatarUri("24x24"));
        avatarUris.put("48x48", user.getAvatarUri("48x48"));
        User my_user = new User(
                user.getSelf(),
                "",
                user.getDisplayName(),
                user.getAccountId(),
                user.getEmailAddress(),
                true,
                user.getGroups(),
                avatarUris,
                user.getTimezone()
        );
        IssueRestClient issueRestClient = cli.getIssueClient();
        IssueInput iib = new IssueInputBuilder()
                .setAssignee(my_user)
                .build();

        issueRestClient.updateIssue("CDE-6496", iib);

        System.out.println(user.toString());
//        assignTicket();
    }

    private static JiraRestClient getJiraRestClient(String login, String password) throws URISyntaxException {
        URI serverUri = new URI("https://burberry.atlassian.net");
        AsynchronousHttpClientFactory asynchronousHttpClientFactory = new AsynchronousHttpClientFactory();
        AuthenticationHandler handler = new BasicHttpAuthenticationHandler(login, password);
        DisposableHttpClient client = asynchronousHttpClientFactory.createClient(serverUri, handler);
        return new AsynchronousJiraRestClient(serverUri, client);
    }


    private static void assignTicket() {
        String command = "curl -D- -u customerinsight@burberry.com:fYNoCX3jSsgNy1YyglSZ59CA -X PUT --data {\\\"accountId\\\":\\\"5e0f4b6db540b70da8386a22\\\"} -H \"Content-Type: application/json\" https://burberry.atlassian.net/rest/api/2/issue/CDE-6496/assignee";
        ProcessBuilder processBuilder = new ProcessBuilder();
        processBuilder.command("/bin/bash", "-c", command);

        try {
            Process process = processBuilder.start();

            StringBuilder output = new StringBuilder();
            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            int exitVal = process.waitFor();
            if (exitVal == 0) {
                System.out.println("Success!");
                System.out.println(output);
                System.exit(0);
            } else {
                System.out.println("Fail");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

    }
}