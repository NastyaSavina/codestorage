/*
 * test.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on Dec 30 2019, 03:45 by COMSOL 5.3.0.316. */
public class test {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model.modelPath("/Users/me/Downloads");

    model.component().create("comp1", true);

    model.component("comp1").geom().create("geom1", 3);

    model.component("comp1").mesh().create("mesh1");

    model.component("comp1").geom("geom1").lengthUnit("km");
    model.component("comp1").geom("geom1").lengthUnit("m");
    model.component("comp1").geom("geom1").scaleUnitValue(true);
    model.component("comp1").geom("geom1").scaleUnitValue(false);
    model.component("comp1").geom("geom1").create("blk1", "Block");
    model.component("comp1").geom("geom1").feature("blk1").set("size", new double[]{0.5, 1, 1});
    model.component("comp1").geom("geom1").feature("blk1").set("pos", new double[]{0.5, 0.5, 1});
    model.component("comp1").geom("geom1").create("blk2", "Block");
    model.component("comp1").geom("geom1").feature("blk2").set("size", new double[]{0.5, 2, 3});
    model.component("comp1").geom("geom1").feature("blk2").set("pos", new double[]{1., 1., 0.});
    model.component("comp1").geom("geom1").create("blk3", "Block");
    model.component("comp1").geom("geom1").feature("blk3").set("size", new double[]{6.5, 52, 43});
    model.component("comp1").geom("geom1").feature("blk3").set("pos", new double[]{15., 13., 20.});
    model.component("comp1").geom("geom1").create("blk4", "Block");
    model.component("comp1").geom("geom1").feature("blk4").set("size", new double[]{6.5, 51232, 43});
    model.component("comp1").geom("geom1").feature("blk4").set("pos", new double[]{15., 14233., 20.});
    model.component("comp1").geom("geom1").run();

    return model;
  }

  public static void main(String[] args) {
    run();
  }

}
