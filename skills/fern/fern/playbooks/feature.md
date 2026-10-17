# Feature

Add or intentionally change behavior. Define the intended contract before
choosing its implementation. A request to remove a capability also changes
behavior and needs explicit acceptance conditions.

1. Establish who needs the change, observable outcomes, relevant edge/failure
   cases, and non-goals. Reuse accepted decisions. Inspect factual questions;
   resolve consequential product choices with the user unless already delegated.
2. Inspect the affected paths and identify data, state ownership, interfaces,
   compatibility requirements, and dependencies. Use an architect for choices
   with substantial downstream cost; a small local feature needs no design
   ceremony. Prototype uncertain behavior only within the task's scope.
3. Implement a useful, verifiable slice. Settle shared contracts and generated
   output ownership before dependent parallel work. Preserve existing behavior
   except where the new acceptance conditions deliberately change it.
4. Exercise the new user or API path and relevant boundary/failure cases. Check
   affected existing behavior and required compatibility. Match the surface to
   the claim: unit tests alone do not prove a visible interaction works.

Use Fern's shared validation and authorized delivery rules. Report the new
behavior, meaningful choices, acceptance evidence, compatibility limits, and
remaining decisions. Unimplemented or unverified acceptance criteria stay open.
