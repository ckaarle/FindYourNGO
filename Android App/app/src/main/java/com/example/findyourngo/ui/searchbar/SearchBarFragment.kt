package com.example.findyourngo.ui.searchbar

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProviders
import com.example.findyourngo.R

class SearchBarFragment : Fragment() {

    companion object {
        fun newInstance() = SearchBarFragment()
    }

    private lateinit var viewModel: SearchBarViewModel

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_search_bar, container, false)
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        viewModel = ViewModelProviders.of(this).get(SearchBarViewModel::class.java)
        // TODO: Use the ViewModel
    }

}