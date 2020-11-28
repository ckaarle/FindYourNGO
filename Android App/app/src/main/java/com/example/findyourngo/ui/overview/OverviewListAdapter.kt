package com.example.findyourngo.ui.overview

import android.app.Activity
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.RatingBar
import android.widget.TextView
import com.example.findyourngo.R
import com.example.findyourngo.models.NGOItem

class OverviewListAdapter(private val context: Context, private val dataSource: ArrayList<NGOItem>): BaseAdapter() {

    private val inflater: LayoutInflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

    override fun getCount(): Int {
        return dataSource.size
    }

    override fun getItem(position: Int): Any {
        return dataSource[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        val rowView = inflater.inflate(R.layout.overview_item, parent, false)

        val ngoName = rowView.findViewById(R.id.overview_item_info_name) as TextView;
        val ngoSiteOfOperation = rowView.findViewById(R.id.overview_item_info_siteofoperation)  as TextView
        val ngoRatingStars = rowView.findViewById(R.id.overview_item_trustworthiness_stars) as RatingBar
        val ngoRatingValue = rowView.findViewById(R.id.overview_item_trustworthiness_rating_ratevalue) as TextView
        val ngoRatingAmount = rowView.findViewById(R.id.overview_item_trustworthiness_rating_amountofrates) as TextView

        val ngoItem = getItem(position) as NGOItem
        ngoName.text = ngoItem.name
        ngoSiteOfOperation.text = ngoItem.siteOfOperation
        ngoRatingValue.text = "(" + ngoItem.value + ")"
        ngoRatingAmount.text = ngoItem.amount.toString()
        ngoRatingStars.rating = ngoItem.value

        return rowView
    }
}