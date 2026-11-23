package com.luna.domain.data.model.home

import com.luna.domain.data.model.home.chart.Chart
import com.luna.domain.data.model.mood.Mood
import com.luna.domain.utils.Resource

data class HomeResponse(
    val homeItem: Resource<ArrayList<HomeItem>>,
    val exploreMood: Resource<Mood>,
    val exploreChart: Resource<Chart>,
)