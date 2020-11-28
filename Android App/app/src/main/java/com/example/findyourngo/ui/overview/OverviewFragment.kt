package com.example.findyourngo.ui.overview

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ListView
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.example.findyourngo.R
import com.example.findyourngo.models.NGOItem

class OverviewFragment : Fragment() {

    private lateinit var overviewViewModel: OverviewViewModel

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        overviewViewModel = ViewModelProviders.of(this).get(OverviewViewModel::class.java)
        val root = inflater.inflate(R.layout.fragment_overview, container, false)

        val overviewFilters: TextView = root.findViewById(R.id.overview_filters)
        overviewViewModel.text.observe(viewLifecycleOwner, Observer {
            overviewFilters.text = it
        })

        val overviewList: ListView = root.findViewById(R.id.overview_list)
        val ngoList = getNGOItems()
        val overviewAdapter = OverviewListAdapter(context!!, ngoList)
        overviewList.adapter = overviewAdapter

        return root
    }

    fun getNGOItems(): ArrayList<NGOItem> {
        val mockNGO = NGOItem("Name", "Site", 2.5f, 10)
        val ngoList = ArrayList<NGOItem>()
        for (x in 0..9) {
            ngoList.add(mockNGO)
        }
        return ngoList
    }
}