"""Final visual-review launcher for the green Range + unified strike marker pass."""

import design_review_demo as review
import club_redesign_v4
import range_redesign_v3


_Parent = review.ReviewDesignApp


class FinalReviewApp(_Parent):
    def draw_3d_range_viewport(self, *args, **kwargs):
        return range_redesign_v3.draw_range(self, *args, **kwargs)

    def draw_top_metric_toolbar(self, *args, **kwargs):
        if self.view_mode == 1:
            return club_redesign_v4.draw_top_metric_toolbar(self, *args, **kwargs)
        return super().draw_top_metric_toolbar(*args, **kwargs)

    def draw_4_quadrant_studio(self, *args, **kwargs):
        # Bypass the older Club wrapper in OverviewDesignApp and hand v4 the
        # actual production renderer, exactly as the design launcher does.
        def production_draw(*a, **k):
            return review.current.base.DesignDemoApp.draw_4_quadrant_studio(
                self, *a, **k
            )

        return club_redesign_v4.draw_4_quadrant_studio(
            self, production_draw, *args, **kwargs
        )


# review.main resolves this module global at runtime, so swapping the class lets
# us reuse all deterministic mock data, sizing, header, and startup behavior.
review.ReviewDesignApp = FinalReviewApp


if __name__ == "__main__":
    review.main()
