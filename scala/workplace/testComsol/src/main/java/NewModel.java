/*
 * NewModel.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on Dec 30 2019, 13:15 by COMSOL 5.3.0.316. */
public class NewModel {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model.modelPath("/Users/me/programs/scala/workplace/testComsol/src/main/java");

    model.comments("untitled\n\n");

    return model;
  }

  public static void main(String[] args) {
    run();
  }

}
