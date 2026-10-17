# Godot 4 Lighting

Read for authoring/reviewing `DirectionalLight3D`, `OmniLight3D`, `SpotLight3D`,
`AreaLight3D`, shadows, global illumination (`SDFGI`, `VoxelGI`, `LightmapGI`,
`SSIL`), `ReflectionProbe`, 2D lights (`PointLight2D`, `DirectionalLight2D`,
`CanvasModulate`, `LightOccluder2D`), or projected `Decal` nodes, which share
the clustered-element budget with lights and probes. Facts follow the official
Godot stable documentation (checked against 4.7); confirm the project's actual
minor version and renderer before relying on items marked
**[version-sensitive]**. Ambient light, sky, tonemap, and exposure live in
`references/rendering-environment.md`.

## Choosing a Light

`Light3D` is abstract; use one of its four subclasses.

| Need | Node | Notes |
| --- | --- | --- |
| Sun or moon | `DirectionalLight3D` | Only rotation matters; strongest shadows (PSSM) |
| Bulb, torch | `OmniLight3D` | Range-limited; pair with distance fade |
| Flashlight, stage light | `SpotLight3D` | Shadows fail above an 89 degree cone; use Omni for wider |
| Window, light box, screen | `AreaLight3D` **[version-sensitive]** | Most expensive real-time light; use sparingly |

`AreaLight3D` is new in recent versions. Before using it, confirm the project's
Godot version has it. Known limits: shadows distort when nearby meshes are
under-subdivided, light leaks at grazing angles on back faces, only Lambertian
diffuse and GGX specular are modeled (anisotropic materials render isotropic),
Compatibility cannot cast area-light shadows, and textured area lights work only
on Forward+ and Mobile. In Forward+, area lights in view add GPU cost to all
rendered objects, so reserve them for cinematics or high-end targets.

## Shared Light Properties

| Property | Default | Review note |
| --- | --- | --- |
| `light_energy` | 1.0 | Not a physical unit unless physical light units are enabled |
| `light_indirect_energy` | 1.0 | Scales GI bounce independently of direct light |
| `light_volumetric_fog_energy` | 1.0 | 0 skips the light's volumetric fog cost |
| `light_specular` | 1.0 | 0 gives diffuse-only |
| `light_negative` | false | Darkens; do not use it as a shadow substitute by reflex |
| `light_size` | 0.0 | Enables PCSS-style softness; see Shadows |
| `light_cull_mask` | all layers | Check it before debugging "light not affecting object" |
| `light_bake_mode` | Dynamic | See GI and Baking |

Physical light units (`rendering/lights_and_shadows/use_physical_light_units`)
switch Omni/Spot to lumens and Directional to lux, and enable
`light_temperature`. Turn them on project-wide or not at all; mixed unit
assumptions break exposure.

## Renderer Limits

Read `rendering/renderer/rendering_method` in `project.godot` first.
**[version-sensitive]**

| Limit | Forward+ | Mobile | Compatibility |
| --- | --- | --- | --- |
| Omni + Spot | Up to 512 clustered elements in view (shared with decals and reflection probes); adjustable | 8 + 8 per mesh; 256 + 256 in view; not adjustable | 8 + 8 per mesh; adjustable with a performance cost |
| `DirectionalLight3D` | 8 | 8 | 8 |
| PCSS / angular-distance soft shadows | yes | no | no |
| Light projector textures | yes | yes | no |
| `ReflectionProbe` per mesh | see class page | 8 | 2 |
| `Decal` | Shares the clustered-element budget | 8 per mesh resource | not supported |

- Extra shadowed directional lights share the atlas and lower each light's
  effective shadow resolution.
- On Mobile and Compatibility lights are evaluated per mesh. A light only
  affects a mesh whose visible AABB intersects it; more than 8 lights on one
  mesh flicker as the camera moves. Deformed meshes may need a larger
  `extra_cull_margin`.
- On Compatibility, lit results with and without shadows can differ; retune
  energy instead of assuming parity.
- Exceeding a per-mesh limit produces flicker or missing lights, not an error.

## Shadows

- `shadow_enabled` defaults to false. A light with no shadow is a common
  intended cost saving; do not enable shadows on every light.
- Bias: acne (streaks or smearing) means bias is too low; Peter-panning (shadow
  detached from the object) means it is too high. Raise `shadow_normal_bias`
  before `shadow_bias`. Defaults: bias 0.1, normal bias 2.0.
- `shadow_opacity` below 1.0 can fake fill light, and `shadow_blur` softens
  edges.
- `DirectionalLight3D` uses parallel-split shadow maps.
  `directional_shadow_mode` is Orthogonal (fastest), 2 Splits, or 4 Splits
  (default, best quality, slowest). An object spanning all four splits renders
  five times. `directional_shadow_max_distance` (default 100) bounds visible
  shadows; shrink it before adding splits. `directional_shadow_blend_splits`
  costs performance.
- Omni shadows use Cube (default, better quality) or Dual Paraboloid (faster,
  lower quality). Spot shadows render one map and are cheaper.
- Contact-hardening (PCSS) shadows come from `light_size` on Omni/Spot/Area and
  `light_angular_distance` on Directional. Enable only on a few key lights and
  expose a quality switch. Forward+ only for Omni/Spot/Directional; the Mobile
  Area-light penumbra does not vary correctly. **[version-sensitive]**
- Shadow quality is project-wide: atlas size (default 4096; 2048 for low-end
  GPUs), filter (Soft Low default through Soft Ultra), and the atlas subdivision
  that defaults to 88 shadowed Omni/Spot lights in view (4 + 4 + 16 + 64 across
  quadrants).
- For many lights, use `distance_fade_*` on Omni and Spot to drop far lights and
  their shadows.

## Global Illumination and Baking

Direct lights only illuminate a surface once. Pick indirect light by renderer
and content, and state the renderer the choice needs.

| Technique | Renderer | Dynamic objects | Notes |
| --- | --- | --- | --- |
| `SDFGI` | Forward+ | Receive only; do not contribute | Least setup; enable in `Environment`; needs Static meshes; costly; camera-relative cascades |
| `VoxelGI` | Forward+ | Receive; Dynamic meshes and lights contribute live (emissive surfaces, indirect light), but only Static geometry is baked into the voxels and dynamic occlusion is not documented | Fast bake; manual extents; thin walls leak; max 8 instances rendered, 2 blended per pixel |
| `LightmapGI` | All renderers | Receive through probes only | Best runtime performance; needs UV2; max 8 instances rendered; baking needs RenderingDevice |
| `SSIL` | Forward+ | Screen-space | Small-scale detail only; complements another method; edge artifacts |
| `ReflectionProbe` | All renderers | Manual | Reflections, weak indirect light |

The introduction page's summary table has listed VoxelGI as available in every
renderer, but the VoxelGI page states Forward+ only. Treat the per-technique
pages as authoritative and verify in the target version. **[version-sensitive]**

Recommended starting points: desktop, try `SDFGI` first and add others only for
a demonstrated gap; mobile and Compatibility, use only `LightmapGI` and
`ReflectionProbe`; otherwise approximate bounce with placed lights.

`light_bake_mode` decides how each light joins GI:

| Mode | Effect |
| --- | --- |
| Disabled | Ignored by baking; cheapest. Use for effect lights. Hiding a light does not exclude it from a bake |
| Static | Contributes to baked GI (direct and indirect for `LightmapGI`); GI does not update at runtime |
| Dynamic | GI updates live; highest cost. `LightmapGI` bakes only indirect light and keeps direct light real-time |

Static contribution also requires meshes to have GI mode Static; Disabled or
Dynamic meshes are ignored by `LightmapGI`.

### SDFGI

- Needs `WorldEnvironment`, an `Environment` with SDFGI on, and Static meshes;
  dynamic occluders and dynamic emissive surfaces are unsupported.
- Watch for leaks without occlusion, visible cascade shifts on fast camera
  moves, brightness drift when `sdfgi_bounce_feedback` exceeds 0.5, and static
  geometry edits that do not relight until the camera moves.
- Transparent materials receive only diffuse GI; sharp reflections need opaque
  surfaces.

### VoxelGI

- Center the node over the area, keep extents as small as possible, rebake after
  static edits, and balance subdivision against cost.
- Fix leaks with thicker geometry or hidden Static blocker meshes; raise bias
  and normal bias cautiously.
- Low quality (4 taps) or half-resolution GI in project settings are the
  performance levers.

### LightmapGI

- Meshes need UV2 with non-overlapping faces. Prefer import setting `Meshes >
  Light Baking = Static Lightmaps`; tune `Lightmap Texel Size` (default 0.2;
  raise for large scenes). Adjust per-instance Lightmap Scale when reusing a
  mesh at different scales.
- Dynamic objects need `LightmapProbe` nodes or generated probes (`Gen Probes >
  Subdiv`). Probes do not store direct light.
- Denoising: JNLM (built-in, GPU) or OIDN (external binaries). Light bleeding:
  adjust bias or enable supersampling. Memory crashes: raise texel size.
- The editor web build cannot bake, only render existing lightmaps.
- Baked outputs are generated assets; follow `references/asset-editing.md` and
  `references/project-hygiene.md` for ownership and version control. A bake is
  not evidence of runtime correctness until run in the target renderer.

### ReflectionProbe

- `update_mode` defaults to Once (radiance over six frames, cheap). Reserve
  Always for at most one probe per scene.
- Defaults: `box_projection` false, `interior` false (true ignores sky),
  `max_distance` 0, `blend_distance` 1.0.
- Per-mesh probe limits are 8 on Mobile (flicker beyond) and 2 on Compatibility
  (extra probes do not render).

## 2D Lighting

| Node | Role |
| --- | --- |
| `PointLight2D` | Omni or spot-style light with a texture |
| `DirectionalLight2D` | Parallel light for sun or moon |
| `CanvasModulate` | Base color for unlit areas; without it scenes look fully bright |
| `LightOccluder2D` | Polygon that casts shadows; the light must also have shadows enabled |

- Defaults: `energy` 1.0, `blend_mode` Add (also Subtract, Mix),
  `shadow_enabled` false, `shadow_filter` None (PCF5 and PCF13 are softer and
  costlier), `range_z_min/max` -1024 to 1024, layer range 0 to 0,
  item cull mask 1. Check the range and cull masks when a light seems to ignore
  a sprite.
- Shadows radiate from the light's center and appear only where the light
  reaches.
- Normal and specular maps go through a `CanvasTexture` on the sprite; raise the
  light's Height or the effect is barely visible.
- Watch `shadow_filter_smooth` for banding.
- Cheaper alternative: additive-blended `Sprite2D` glows. They cast no shadows
  and cannot properly lighten dark areas.

## Decals

`Decal` projects textures onto meshes inside its box without new geometry, so it
can be moved often at low cost. Use it for dirt, weathering, bullet holes, or
blob shadows on uneven or arbitrary surfaces.

- Channels: Albedo (its alpha masks the other maps), Normal, ORM, Emission.
  Custom shaders and height-based effects are not supported.
- Renderers: Forward+ and Mobile only; Compatibility does not support `Decal`.
  **[version-sensitive]**
- Budget: in Forward+ decals share the clustered-element limit with Omni/Spot
  lights and reflection probes; on Mobile the limit is 8 per mesh resource and
  extras flicker. Failure is silent, so count decals together with lights.
- A decal cannot change the transparency of the surface under it; translucent
  areas stay translucent.
- Defaults: `size` 2 x 2 x 2, `albedo_mix` up to 1.0, `distance_fade_begin` 40
  and `distance_fade_length` 10 (`distance_fade_enabled` must be on),
  `cull_mask` all layers. `normal_fade` limits projection on surfaces facing
  away from the box; `upper_fade` and `lower_fade` soften the box edges.
- Cost is driven by screen coverage: a few large decals cost more than many
  small scattered ones. Enable distance fade, keep the projection depth short so
  culling works, and use `cull_mask` to keep decals off characters or unrelated
  meshes.
- Overlapping decals order with `sorting_offset`; check it before adding extra
  decals to hide an ordering artifact.
- For a flat, fixed surface, a `Sprite3D` or a `QuadMesh` with a transparent
  material avoids the decal budget, but it fits only one plane, can z-fight when
  coplanar, and does not follow relief. Choose it on that basis, not as a
  general replacement.

## Common Failure Signals

| Symptom | Check |
| --- | --- |
| Dark at runtime, fine in editor | Editor preview sun/environment; add explicit light and `WorldEnvironment` |
| Light has no effect on an object | `light_cull_mask`, per-mesh light limits, light range, renderer |
| Lights flicker as the camera moves | More than 8 Omni/Spot on a mesh (Mobile/Compatibility), more than 8 GI instances, probe limits |
| Shadow streaks | Bias too low; raise normal bias |
| Shadow detached from object | Bias too high |
| Shadows vanish at distance | `directional_shadow_max_distance`, fade settings, `distance_fade_shadow` |
| Spot shadow broken | Cone above 89 degrees; use Omni |
| No GI effect | Renderer support, mesh GI mode, light bake mode, `Environment` toggle |
| GI leaks | Thin walls, SDFGI occlusion, VoxelGI extents, blockers |
| Lightmap missing or wrong | UV2, Static mesh and light modes, probe generation, more than 8 instances |
| 2D light has no shadow | `LightOccluder2D` present, light `shadow_enabled`, cull masks |
| Whole 2D scene fully bright | Missing `CanvasModulate` |
| Decal missing or flickering | Renderer (not Compatibility), Mobile 8-per-mesh limit, clustered budget, `cull_mask`, distance fade |

## Validation Expectations

- Static: chosen light types, GI method, and features exist in the configured
  renderer and Godot version; bake modes and mesh GI modes agree; light counts
  respect the renderer limits.
- Runtime: capture with the project's configured renderer and compare against
  the editor viewport. Headless or dummy-renderer runs do not prove lighting
  output, and a bake command succeeding does not prove visual acceptance.
- Report static reasoning, engine runs, and visual acceptance separately.
