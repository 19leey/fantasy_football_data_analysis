library(ggplot2)


# constants
overall <- c("output/consensus/clustered/clustered_overall_rankings_1.csv",
            "output/consensus/clustered/clustered_overall_rankings_2.csv",
            "output/consensus/clustered/clustered_overall_rankings_3.csv")
qb <- "output/consensus/clustered/clustered_qb_rankings.csv"
rb <- "output/consensus/clustered/clustered_rb_rankings.csv"
wr <- "output/consensus/clustered/clustered_wr_rankings.csv"
te <- "output/consensus/clustered/clustered_te_rankings.csv"
k <- "output/consensus/clustered/clustered_k_rankings.csv"
dst <- "output/consensus/clustered/clustered_dst_rankings.csv"


get_positions <- function() {
  positions <- vector(mode="list", length=6)
  positions[[1]] <- c("qb", qb)
  positions[[2]] <- c("rb", rb)
  positions[[3]] <- c("wr", wr)
  positions[[4]] <- c("te", te)
  positions[[5]] <- c("k", k)
  positions[[6]] <- c("dst", dst)
  positions
}


get_title <- function(position) {
  if (position == 'qb') {
    "Quarterback"
  } else if (position == 'rb') {
    "Running Back"
  } else if (position == 'wr') {
    "Wide Receiver"
  } else if (position == 'te') {
    "Tight End"
  } else if (position == 'k') {
    "Kicker"
  } else {
    "Defense"
  }
}


render_tiers <- function(file_path, position) {
  if (missing(position)) {
    df <- read.csv(file_path)
    x_min = (min(df$Rank) - 20)
    if (x_min < 0) {
      x_min = -5
    }
    tiers_plot <- ggplot(df, aes(x=Avg, y=Rank, label=Name)) +
      geom_errorbarh(aes(xmin = Avg - Std.Dev/2, xmax = Avg + Std.Dev/2, colour=factor(Tiers)), alpha=0.4) +
      geom_point() +
      geom_text(aes(label=Name, x=Avg - Std.Dev/2, colour=factor(Tiers)), hjust=1.1, vjust=0.5, size=3.0) +
      geom_text(aes(label=Pos, x=Avg + Std.Dev/2, colour=factor(Tiers)), hjust=-0.4, vjust=0.5, size=3.0) +
      labs(x="Expert Consensus Average", y="Expert Consensus Rank") +
      ggtitle("2018 Overall Rankings Tiers") + theme(plot.title = element_text(hjust = 0.5)) +
      scale_colour_discrete(name="Tiers") +
      expand_limits(x = x_min) +
      scale_y_reverse()
    tiers_plot
  }
  else {
    df <- read.csv(file_path)
    title <- sprintf("2018 %s Rankings Tiers", get_title(position))
    tiers_plot <- ggplot(df, aes(x=Avg, y=Rank, label=Name)) +
      geom_errorbarh(aes(xmin = Avg - Std.Dev/2, xmax = Avg + Std.Dev/2, colour=factor(Tiers)), alpha=0.4) +
      geom_point() +
      geom_text(aes(label=Name, x=Avg - Std.Dev/2, colour=factor(Tiers)), hjust=1.1, vjust=0.5, size=3.0) +
      labs(x="Expert Average Rank", y="Expert Consensus Rank") +
      ggtitle(title) + theme(plot.title = element_text(hjust = 0.5)) +
      scale_colour_discrete(name="Tiers") +
      expand_limits(x = -5) +
      scale_y_reverse()
    tiers_plot
  }
}


run_script <- function() {
  plots_dir_path <- "output/plots/"
  slice_index = 1
  for (slice in overall) {
    filename <- sprintf("%soverall_rankings_%s.png", plots_dir_path, slice_index)
    ggsave(filename, plot=render_tiers(slice), width=320, height=230, units="mm")
    slice_index = slice_index + 1
  }

  for (file in get_positions()) {
    filename <- sprintf("%s%s_rankings.png", plots_dir_path, file[1])
    ggsave(filename, plot=render_tiers(file[2], file[1]), width=320, height=230, units="mm")
  }
}


run_script()
