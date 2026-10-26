# Site analytics

The course uses a separate site under Rajiv's existing GoatCounter account:
<https://learn-harness-engineering.goatcounter.com/>. The dashboard requires login.

The integration lives in `docs/.vitepress/theme/analytics.ts` and is installed
by the VitePress theme. It runs only on `rajshah4.github.io` under
`/learn-openhands-harness/`, so local development and previews do not send data.

It records the first page view and subsequent VitePress route changes. Section
links on the same page do not create additional page views. GoatCounter records
referrers using its normal page-view behavior.

Click events cover PDF and ZIP downloads, GitHub links, and YouTube, Instagram,
and Vimeo links. Download classification takes priority over GitHub classification.
Event names contain the destination and source page so clicks from different
lessons can be compared. Destination query strings and fragments are omitted,
except the YouTube video ID needed to identify a watch link. These are click
counts, not completed downloads or video plays. Standalone HTML files outside
the VitePress theme do not receive this integration.

Ad blockers can prevent tracking. Treat totals as a lower bound. GitHub release
asset download counts remain a separate useful measure. No analytics credentials
are stored in the repository.

To verify a deployment, use a browser without a GoatCounter blocker, visit a few
course pages, and click a resource link. Check the dashboard for both page paths
and events. Test clicks will be included in the counts.
