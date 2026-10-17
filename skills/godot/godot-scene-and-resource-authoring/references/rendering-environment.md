# Godot 4 Rendering Environment

Read for authoring/reviewing `WorldEnvironment`, `Environment`,
`CameraAttributes*`, `Compositor`, sky, fog, glow, tonemap, exposure, depth of
field, or renderer-dependent visual settings in 3D scenes. Facts follow the
official Godot 4.x class references and 3D post-processing tutorial; confirm the
project's actual minor version and renderer before relying on items marked
**[version-sensitive]**.

## Ownership and Precedence

`WorldEnvironment` is a Node with no behavior of its own. It holds three
optional scene-default Resources:

| Property | Type | Controls |
| --- | --- | --- |
| `environment` | `Environment` | Background, sky, ambient/reflected light, tonemap, glow, fog, SSAO/SSR/SSIL/SDFGI, adjustments |
| `camera_attributes` | `CameraAttributes` | Exposure, auto exposure, depth of field |
| `compositor` | `Compositor` | Custom `CompositorEffect` list |

The active `Camera3D` has its own `environment`, `attributes`, and `compositor`.
A camera-assigned Resource overrides the `WorldEnvironment` value for that
camera; the project default environment applies when neither is set. Before
debugging a `WorldEnvironment`, check `Camera3D` overrides first.

- Only one `WorldEnvironment` may exist in a scene. Search the main scene,
  instanced sub-scenes, and autoload scenes before adding one.
- A `WorldEnvironment` with an empty `environment` has no effect.
- Prefer scene-default Resources for general setup; use camera-level Resources
  only for intentional local overrides such as an underwater view.
- Decide shared `.tres` versus scene-local sub-resource by reuse and ownership,
  following project convention.

## Editor Preview Is Not Runtime

When a scene has no `WorldEnvironment` and no `DirectionalLight3D`, the editor
shows a preview environment and sun. That preview does not exist in the running
project. A scene that looks lit in the editor viewport can be dark or wrong at
runtime, so the viewport alone is not evidence. Author explicit environment and
light Nodes, or use the editor's preview buttons to add them to the scene, then
confirm with a real run through `$godot-build-and-diagnostics`.

## Renderer Support

Read `rendering/renderer/rendering_method` (and platform overrides) in
`project.godot` before enabling features. **[version-sensitive]**

| Feature | Forward+ | Mobile | Compatibility |
| --- | --- | --- | --- |
| Sky, ambient, tonemap, fog, adjustments | yes | yes | yes |
| Glow | full | simplified | simplified |
| SSAO | yes | no | yes |
| SSR, SSIL, SDFGI | yes | no | no |
| Auto exposure | yes | no | no |
| Depth of field | yes | yes | no |
| Compositor / `CompositorEffect` | yes | yes | no |

Volumetric fog is a Forward+ feature by general Godot knowledge but is not in
the official `Environment` support table; verify against its class page when it
matters.

An unsupported property usually has no effect and no error, so a missing warning
does not prove the effect works. SSR and depth of field do not work on
transparent-background viewports. Screen-space effects (SSR, SSAO, SSIL, glow)
cannot see off-screen or occluded geometry. Fog can band.

## Environment Settings

Post-processing order: depth of field, auto exposure, glow, tonemap,
adjustments.

- **Background/sky**: `background_mode = Sky` needs an assigned `sky`. Use
  `Canvas` mode for 2D scenes that need glow or adjustments.
- **Light sources**: pair `ambient_light_source` and `reflected_light_source`
  with the intended source (for example Sky) and a `DirectionalLight3D` for
  direct light. The default ambient color is black.
- **Tonemap**: Linear is cheapest and blows out highlights; ACES and AgX are
  more realistic at higher cost. The docs recommend `tonemap_white` of 6.0 to
  8.0 for photorealistic lighting. Filmic and ACES output SDR only. AgX is a
  recent addition. **[version-sensitive]**
- **Glow**: subtle and off by default. It appears only when values exceed
  `glow_hdr_threshold` or `glow_bloom` is above 0.0. On Mobile, Compatibility,
  and 2D, lower the threshold below 1.0.
- **Adjustments**: `adjustment_enabled` must be true for brightness, contrast,
  saturation, or LUT to apply. Brightness applies after tonemapping. LUTs are
  SDR only.
- **Fog**: `fog_depth_end = 0` means camera far. Volumetric fog is separate and
  more expensive; do not enable both by reflex.
- **SDFGI**: meshes need sufficiently thick walls to avoid light leaks;
  `sdfgi_bounce_feedback` above 0.5 risks runaway lighting.
- SSAO, SSR, SSIL, and SDFGI default to off and cost GPU time; enable only what
  the task needs and state the required renderer.

## CameraAttributes

Use one subclass:

- `CameraAttributesPractical`: near/far depth of field by distance and
  transition (negative transition means physically based), plus ISO
  auto-exposure limits.
- `CameraAttributesPhysical`: aperture, shutter speed, focal length, focus
  distance, frustum near/far, and EV100 auto-exposure limits. Attached to a
  `Camera3D`, it overrides that camera's `near`, `far`, `fov`, and
  `keep_aspect`, so tuning those on the camera has no effect.

Base exposure settings (`exposure_multiplier`, `exposure_sensitivity`, auto
exposure) apply to both. On `VoxelGI` and `LightmapGI`, only exposure settings
apply. Auto exposure is Forward+ only; depth of field is Forward+ and Mobile.

## Compositor

`Compositor` and `CompositorEffect` are experimental; the API may change between
minor versions. **[version-sensitive]** They reach only 3D pipeline stages.

- Prefer built-in `Environment` effects. Use a compositor effect only when a
  built-in cannot express the effect or it needs depth, normal, or motion
  buffers.
- `_render_callback` runs on the rendering thread: no scene tree access, and
  guard data shared with the main thread with a `Mutex`.
- Request only needed buffers (`access_resolved_color/depth`,
  `needs_motion_vectors`, `needs_normal_roughness`, `needs_separate_specular`).
  Normal/roughness and separate specular are Forward+ only.
- Create shaders, pipelines, and uniform sets once and cache them; free shader
  RIDs on `NOTIFICATION_PREDELETE`.
- Runtime-compiled GLSL cannot be precompiled or cached, which is a risk on
  consoles; prefer precompiled `.glsl` for shipped effects.
- Do not use compositor effects in a project that targets Compatibility.

Light nodes, shadows, GI baking, and reflection probes are covered in
`references/lighting.md`.

## Common Failure Signals

| Symptom | Check |
| --- | --- |
| Dark at runtime, fine in editor | Missing explicit `WorldEnvironment` or light |
| Settings ignored | `Camera3D` override, or second `WorldEnvironment` |
| Effect does nothing | Renderer support, `adjustment_enabled`, glow threshold/bloom |
| Sky invisible | `background_mode` and `sky` assignment |
| Camera `near`/`far`/`fov` edits ignored | `CameraAttributesPhysical` on that camera |
| Auto exposure ignored | Not Forward+ |

## Iterating on Visual Feedback

For feedback such as washed-out color, flat forms, or objects looking pasted
into the scene, distinguish exposure and color from light/shadow plane
separation, contact shadows, spatial occlusion, and material response before
choosing settings. Check representative lit, shaded, and contact regions; a
visually floating object may have a geometry gap or a detached shadow. Use
`references/lighting.md` for the relevant light and shadow controls.

Keep a baseline capture and hold the camera and unrelated rendering conditions
fixed while changing one related group of settings. Compare the full frame and
representative details against the reference and earlier user requirements after
each iteration: opening shadows should not erase form, and stronger contact
should not reintroduce crushed dark areas. Brightness statistics and passing
geometry checks support diagnosis but do not establish visual acceptance. Treat
numeric settings and proposed remedies as scene-specific trials until the
rendered result supports them.

## Validation Expectations

- Static: exactly one `WorldEnvironment` in the loaded tree, `environment`
  assigned, enabled features supported by the configured renderer, and dependent
  properties set.
- Runtime: capture from the project's configured renderer and compare against
  the editor viewport. Headless or dummy-renderer runs do not prove visual
  output.
- Report static reasoning, engine runs, and visual acceptance separately.
