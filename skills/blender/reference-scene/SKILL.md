---
name: reference-scene
description: >-
  Reconstruct an editable Blender environment from visual references while
  preserving layout, proportions, style, and credible unseen structure. Use for
  scene blockout, detailed reconstruction, and multi-view review; not for image
  generation or Unreal import alone.
---

# Reference Scene

Deliver an editable scene that works throughout the user's requested viewing
range. References guide art; confirmed design and user instructions determine
purpose. Do not automatically turn arrows, labels, or zone diagrams into
physical objects.

1. Follow [reconstruction methods][link-1] to distinguish visible facts,
   estimates, and inferred backsides. Establish layout anchors, silhouettes,
   scale evidence, material families, and permitted adjustments.
2. Use a few large volumes to check positions, proportions, entrances, and
   circulation. Inspect the main view, rear, sides, and actual viewing height
   before adding detail.
3. Complete supports, thickness, backsides, and local orientation for the
   intended use. Follow [geometry and multiple-view validation][link-2];
   screen-space contact does not prove a sound structure.
4. Render the complete scene to inspect color blocks, occlusion, silhouettes,
   and materials. Temporarily hiding objects can aid diagnosis; record
   visibility in delivery evidence and do not hide defects to claim complete
   reconstruction.
5. Separate environment, references, rulers, cameras, and presentation objects.
   Identify the source of truth for generators and manual edits. Pack
   dependencies or deliver relative textures, then reopen to verify.
6. For engine delivery, choose representations that can be exported or baked.
   Geometry Nodes, instances, procedural textures, and modifiers can author the
   source; exchange outputs must work in the target engine. Use available
   `$blender-to-unreal-scene` for UE migration. Blender previews do not replace
   engine acceptance.

## Tools

- [audit_scene.py][link-3]: inspect evaluated meshes, UVs, materials, topology,
  and optional usage constraints in a specified collection. Judge open surfaces
  by their purpose.
- [scene_components.py][link-4]: parameterized components and Blender assembly;
  see [component usage][link-5]. Procedural generation is optional.
- [build_example.py][link-6]: two examples with different dimensions, layouts,
  and orientations, written to new files. These validate tools; they are not
  product templates.

UV presence, absence of non-manifold edges, or a fixed screenshot count alone
cannot establish completion. Check reference fidelity, physical space,
dependencies, and viewing range together.

[link-1]: references/reconstruction.md
[link-2]: references/validation.md
[link-3]: scripts/audit_scene.py
[link-4]: scripts/scene_components.py
[link-5]: references/components.md
[link-6]: scripts/build_example.py
